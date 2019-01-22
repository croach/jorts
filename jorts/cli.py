#!/usr/bin/env python

"""
Script to convert a Jupyter notebook to a PDF.

This script will convert a Jupyter notebook to a PDF and offers the option of
moving inline cell contents out of the body of the report and into a separate
appendix section. The inspiration for this functionality comes from the R
community's knitr and R Markdown projects. An example of which can be seen in
the blog post from the creator of knitr listed below.

https://yihui.name/en/2018/09/code-appendix/

To use the appendix feature, just add a label to any cell's metadata, and then
reference that label in the "ref_labels" list of the metadata of the cell where
you want to display the contents later in the notebook. To also hide the
contents of the cell inline, add a "hide_all" tag to its metadata. An example of
the metadata for a cell that both adds a label and hides the contents can be
seen below.

  {
    "tags": [
      "hide_all"
    ],
    "label": "appendix"
  }

To display the cell contents in an appendix, simply add a cell later in the
notebook and add the labels of the cells that you want to display in the
"ref_labels" list. An example of the metadata of a cell that displays the
labeled cell contents is given below.

  {
    "ref_labels": [
      "appendix"
    ]
  }

The labeled cell contents will be stitched together in order of their appearance
in the document.

Note that, unlike the R Markdown and knitr versions of this feature, this script
allows users to reuse labels throughout the notebook. In that sense, they act a
bit more like tags than they do labels; however, you can only have a single
label, whereas a cell can have several tags.

"""
import nbformat

import argparse
import os

from jorts.converter import convert_notebook_to_pdf


# The nbformat version to write. Use this to downgrade notebooks. The choices
# are 1,2,3,4 and the default is 4.
NBFORMAT_VERSION = 4

def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__)
  parser.add_argument('notebook', type=str,
                      help='Notebook file to be converted')
  parser.add_argument('--template', dest='template_file', type=str,
                      help='Optional template file')
  parser.add_argument('--output', dest='output_file', type=str,
                      help='Name of the output file')
  args = parser.parse_args()

  # Pull the code from the notebook, add it to the appendix, and convert the
  # notebook to a PDF file
  model = {
    'content': nbformat.read(args.notebook, as_version=NBFORMAT_VERSION),
    'type': 'notebook',
    'name': args.notebook
  }
  output_file = os.path.splitext(args.notebook)[0] + '.pdf'
  body = convert_notebook_to_pdf(model, args.template_file)
  with open(args.output_file, 'wb') as fout:
    fout.write(body)
