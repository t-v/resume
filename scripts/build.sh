#!/usr/bin/env bash
#
# Builds the resume to HTML, PDF, DOCX and Markdown with yamlresume, then
# applies the personal branding on top of the stock templates.
#
# Everything runs inside the official yamlresume image so that local builds and
# CI builds are byte-for-byte comparable: it ships XeTeX, the moderncv/ctex/
# fontawesome packages and the Linux Libertine fonts that the LaTeX layout needs.
#
# Usage:
#   ./scripts/build.sh                      # build resume/t-v-resume.yml into output/
#   RESUME=resume/other.yml ./scripts/build.sh
#
# Environment:
#   RESUME             resume source file   (default: resume/t-v-resume.yml)
#   OUTPUT_DIR         output directory     (default: output)
#   YAMLRESUME_IMAGE   pinned builder image (default: yamlresume/yamlresume:v0.16.2)
#   BUILD_DATE         date stamp in the HTML footer (default: today, UTC)
#
# RESUME and OUTPUT_DIR must be relative to the repository root: only the
# repository is mounted into the container, so an absolute path would make
# yamlresume write into the container's own filesystem and silently lose the
# artifacts.

set -euo pipefail

RESUME="${RESUME:-resume/t-v-resume.yml}"
OUTPUT_DIR="${OUTPUT_DIR:-output}"
YAMLRESUME_IMAGE="${YAMLRESUME_IMAGE:-yamlresume/yamlresume:v0.16.2}"

BASENAME="$(basename "${RESUME}")"
BASENAME="${BASENAME%.*}"
STEM="${OUTPUT_DIR}/${BASENAME}"

for var in RESUME OUTPUT_DIR; do
  case "${!var}" in
    /* | */../* | ../*)
      echo "error: ${var}='${!var}' must be a relative path inside the repository" >&2
      exit 1
      ;;
  esac
done

if [ ! -f "${RESUME}" ]; then
  echo "error: resume '${RESUME}' not found" >&2
  exit 1
fi

mkdir -p "${OUTPUT_DIR}"

# Run the image as the calling user so the generated files are not root owned,
# both on a workstation and on a GitHub Actions runner.
docker_run() {
  docker run --rm \
    -u "$(id -u):$(id -g)" \
    -e HOME=/tmp \
    -v "${PWD}":/home/yamlresume \
    "$@"
}

# 1. Validate. Neither `yamlresume validate` nor `yamlresume build` signals a
#    schema violation through its exit code: both happily exit 0 and keep
#    rendering. The only reliable gate is the summary line, so match on it.
echo "==> Validating ${RESUME}"
validation="$(docker_run -w /home/yamlresume "${YAMLRESUME_IMAGE}" \
  validate "${RESUME}" 2>&1 || true)"
echo "${validation}"

if ! grep -q 'Resume validation passed' <<<"${validation}"; then
  echo "error: ${RESUME} does not satisfy the YAMLResume schema" >&2
  exit 1
fi

# 2. Build every layout. The PDF is deliberately skipped here: the .tex needs to
#    be recoloured before it is compiled, because moderncv only exposes named
#    colour schemes and yamlresume cannot override them through the schema.
echo "==> Building ${RESUME}"
docker_run -w /home/yamlresume "${YAMLRESUME_IMAGE}" \
  build "${RESUME}" --no-pdf --no-validate -o "${OUTPUT_DIR}"

# 3. Brand the generated HTML and LaTeX.
echo "==> Theming"
node scripts/apply-theme.mjs "${STEM}"

# 4. Compile the recoloured .tex. The image has no Quicksand, so fonts/ is
#    mounted in and the font cache is rebuilt before XeTeX resolves
#    \setmainfont{Quicksand}. Runs twice so moderncv's layout and any
#    references settle, same as a normal latexmk pass would.
echo "==> Compiling PDF"
docker_run \
  -v "${PWD}/fonts":/usr/share/fonts/truetype/quicksand:ro \
  -w "/home/yamlresume/${OUTPUT_DIR}" \
  --entrypoint sh "${YAMLRESUME_IMAGE}" -euc \
  "fc-cache -f > /dev/null 2>&1
   for _ in 1 2; do
     xelatex -interaction=nonstopmode -halt-on-error '${BASENAME}.tex' > /dev/null
   done"

# 5. Drop the LaTeX scratch files, keep the artifacts.
rm -f "${STEM}.aux" "${STEM}.log" "${STEM}.out" "${STEM}.toc"

echo "==> Done"
ls -lh "${STEM}".* | sed 's/^/    /'
