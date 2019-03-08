#!/usr/bin/env python

from docx import Document
import textract

text = textract.process('output/resume.docx', extension='docx')

for line in str(text).split('\n'):
    if "{{" in line or "}}" in line:
        raise "Not all template variables have been resolved"
    #print line

# text = textract.process('output/resume.md', extension='md')

for line in str(text).split('\n'):
    if "{{" in line or "}}" in line:
        raise "Not all template variables have been resolved"
    #print line
