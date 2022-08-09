#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import json
import os
import markdown
import pdfkit
from jinja2 import Environment, FileSystemLoader

def get_context(resumedir, filename):
    if os.path.splitext(filename)[1] in ['.yml', '.yaml']:
        context = yaml.load(open(resumedir + "/" + filename, 'r', encoding="utf-8"), Loader=yaml.SafeLoader)
    elif os.path.splitext(filename)[1] in ['.json']:
        context = json.loads(open(resumedir + "/" + filename, 'r', encoding="utf-8").read())
    else:
        print(os.path.splitext(filename)[1] + " is not a valid source file.")
        context = {}
    # print(yaml.dump(context, encoding=('utf-8')))
    return context

def generate_md(outputdir, context, md):
    env = Environment(loader = FileSystemLoader(os.path.dirname(os.path.abspath(__file__))), trim_blocks=True)
    template = env.get_template(md)
    with open(outputdir + "/" + os.path.splitext(filename)[0] + ".md", 'w+', encoding="utf-8") as x_file:
        rendered_template = template.render(context)
        x_file.write(rendered_template)
        return rendered_template

def generate_html(outputdir, context, html):
    env = Environment(loader = FileSystemLoader(os.path.dirname(os.path.abspath(__file__))), trim_blocks=True)
    # env.filters["md2html"] = md2html
    template = env.get_template(html)
    with open(outputdir + "/" + os.path.splitext(filename)[0] + ".html", 'w+', encoding="utf-8") as x_file:
        rendered_template = template.render(context)
        x_file.write(rendered_template)
        return rendered_template

# def generate_docx(outputdir, context, docx):
#     template = DocxTemplate(docx)
#     template.render(context)
#     template.save(outputdir + "/" + os.path.splitext(filename)[0] + ".docx")

if __name__ == '__main__':
    md = "templates/cv_template.j2.md"
    html = "templates/cv_template.j2.html"
    outputdir = os.getcwd() + "/output"
    resumedir = os.getcwd() + "/resume"
    config = pdfkit.configuration(wkhtmltopdf="C:\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

    for r, d, filenames in os.walk(resumedir):
        for filename in filenames:
            print(filename)
            context = get_context(resumedir, filename)
            if context != {}:
                markdown_content = generate_md(outputdir, context, md)
                #print(markdown_content)
                html_content = generate_html(outputdir, context, html)
                pdfkit.from_file(outputdir + "/" + os.path.splitext(filename)[0] + ".html", outputdir + "/" + os.path.splitext(filename)[0] + ".pdf", configuration=config)

