#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docxtpl import DocxTemplate
from jinja2 import Environment, FileSystemLoader
import yaml
import json
import os

def get_context(resumedir, filename):
    if os.path.splitext(filename)[1] in ['.yml', '.yaml']:
        context = yaml.load(open(resumedir + "/" + filename, 'r', encoding="utf-8"))
    elif os.path.splitext(filename)[1] in ['.json']:
        context = json.loads(open(resumedir + "/" + filename, 'r', encoding="utf-8").read())
    else:
        print(os.path.splitext(filename)[1] + " is not a valid source file.")
        context = {}
    print(yaml.dump(context, encoding=('utf-8')))
    return context

def generate_md(outputdir, context, template):
    env = Environment(loader = FileSystemLoader(os.path.dirname(os.path.abspath(__file__))), trim_blocks=True)
    template = env.get_template(template)
    with open(outputdir + "/" + os.path.splitext(filename)[0] + ".md", 'w+', encoding="utf-8") as x_file:
        rendered_template = template.render(context)
        x_file.write(rendered_template)

def generate_docx(outputdir, context, template):
    template.render(context)
    template.save(outputdir + "/" + os.path.splitext(filename)[0] + ".docx")

docx = DocxTemplate("templates/cv_template.docx.j2")
md = "templates/cv_template.md.j2"
outputdir = os.getcwd() + "/output"
resumedir = os.getcwd() + "/resume"

for r, d, filenames in os.walk(resumedir):
    for filename in filenames:
        print(filename)
        context = get_context(resumedir, filename)
        if context != {}:
            generate_md(outputdir, context, md)
            generate_docx(outputdir, context, docx)
