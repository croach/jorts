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


def convert_notebook_to_pdf(notebook, output_file=None, template_file=None):
  config = get_config()
  exporter = nbconvert.PDFExporter(config)
  if template_file is not None:
    exporter.template_file = template_file

  notebook = nbformat.notebooknode.from_dict(notebook)
  notebook = append_cell_contents(notebook)
  title = os.path.splitext(os.path.basename(output_file))[0]
  resources = nbconvert.exporters.exporter.ResourcesDict()
  resources['metadata'] = {'name': title}
  (body, resources) = exporter.from_notebook_node(notebook, resources)

  with open(output_file, 'wb') as fout:
    fout.write(body)
