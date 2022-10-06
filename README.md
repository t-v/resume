# Generation script for a resume

[![Release Resume](https://github.com/t-v/resume/actions/workflows/release_artifacts.yml/badge.svg)](https://github.com/t-v/resume/actions/workflows/release_artifacts.yml)
[![Deploy static content to Pages](https://github.com/t-v/resume/actions/workflows/pages.yml/badge.svg)](https://github.com/t-v/resume/actions/workflows/pages.yml)


The HTML version of the generated resume: <https://t-v.github.io/resume/>

The PDF or Markdown versions are available for download here: <https://github.com/t-v/resume/releases/latest>


## Prerequisites

Install python: <https://www.python.org/downloads/>

Install the prerequisites:

``` bash
pip install -r requirements.txt
```

Install the font: <https://fonts.google.com/specimen/Quicksand>

## Usage

Make a resume based on the YAML or JSON template and save it in the `resume` directory.
After that, run the generator:

``` bash
python ./generate_resume_generator.py
```

Yes, it is __this__ easy.
