import os
from collections import namedtuple

import nbconvert
import nbformat

try:
    from nbconvert.nbconvertapp import NbConvertApp
except ImportError:
    from IPython.nbconvert.nbconvertapp import NbConvertApp


# The nbformat version to write. Use this to downgrade notebooks. The choices
# are 1,2,3,4 and the default is 4.
NBFORMAT_VERSION = 4


def get_config():
    """Load and return the user's nbconvert configuration
    """
    app = NbConvertApp()
    app.load_config_file()
    return app.config


def append_cell_contents(notebook):
  """Appends prior cell contents to a later cell dependent on labels

  This function will iterate through a notebook and grab all cells that have a
  label and add them to any cell that references that label (i.e., has the label
  in its ref_labels list). Each cell's content will be displayed according to
  the order of its appearance in the notebook.

  """
  Cell = namedtuple('Cell', ['label', 'contents'])
  cells = []
  for cell in notebook['cells']:
    label = cell.get('metadata', {}).get('label', None)
    ref_labels = cell.get('metadata', {}).get('ref_labels', [])
    if label is not None:
      cells.append(Cell(label, cell['source']))
    elif ref_labels:
      cell['source'] = '\n\n'.join(cell.contents for cell in cells if cell.label in ref_labels).strip()

  return notebook


def convert_notebook_to_pdf(model, template_file=None):
  config = get_config()
  exporter = nbconvert.PDFExporter(config)
  # Hide input and output prompts (e.g., In [32]: ) from the exported content
  exporter.exclude_input_prompt = True
  exporter.exclude_output_prompt = True
  if template_file is not None:
    exporter.template_file = template_file

  notebook = nbformat.notebooknode.from_dict(model['content'])
  notebook = append_cell_contents(notebook)
  notebook_name = os.path.splitext(model.get('name', 'Notebook'))[0]
  # For some reason the from_notebook_node function does not bother to use the
  # notebook's metadata, so we need to extract it from the notebook, add it to
  # the resources dict, and pass it in directly.
  resources = nbconvert.exporters.exporter.ResourcesDict()
  resources['metadata'] = dict({'name': notebook_name}, **notebook['metadata'])
  (body, resources) = exporter.from_notebook_node(notebook, resources)

  return body


def _convert_notebook_to_pdf(notebook, output_file=None, template_file=None):
  body = convert_notebook_to_pdf(notebook, template_file)
  with open(output_file, 'wb') as fout:
    fout.write(body)
