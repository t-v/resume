#!/usr/bin/env python

from docx import Document
import textract

text = textract.process('output/resume.docx', extension='docx')

faulty = False
for line in str(text).split('\n'):
    if "{{" in line or "}}" in line:
        faulty = True
        print(line)
    #print line

if faulty:
    print("Not all template variables have been resolved")
    raise

# text = textract.process('output/resume.md', extension='md')

faulty = False
for line in str(text).split('\n'):
    if "{{" in line or "}}" in line:
        faulty = True
        print(line)
    #print line

if faulty:
    print("Not all template variables have been resolved")
    raise
