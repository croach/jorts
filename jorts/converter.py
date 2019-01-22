import os
import collections

import nbconvert
import nbformat
from traitlets.config.loader import Config

try:
    from nbconvert.nbconvertapp import NbConvertApp
except ImportError:
    from IPython.nbconvert.nbconvertapp import NbConvertApp


# The nbformat version to write. Use this to downgrade notebooks. The choices
# are 1,2,3,4 and the default is 4.
NBFORMAT_VERSION = 4

def convert_notebook_to_pdf(model, template_file=None):
  config = _get_config(default={
    'TagRemovePreprocessor': {
      'remove_all_outputs_tags': {"hide_output"},
      'remove_input_tags': {"hide_input"},
      'remove_cell_tags': {"hide_all"}
    }
  })
  # I believe i may be able to use this to add my own template to the those
  # available. That way I can use it, and users can extend it.
  #config['Exporter']['template_path'].append('my_template_path)
  exporter = nbconvert.PDFExporter(config)
  # Hide input and output prompts (e.g., In [32]: ) from the exported content
  # For some reason, setting exclude_input_prompt = True is causing the
  # newlines in the code to dissapear. This appears to be a bug in nbconvert.
  # exporter.exclude_input_prompt = True
  # exporter.exclude_output_prompt = True

  if template_file is not None:
    exporter.template_file = template_file

  notebook = nbformat.notebooknode.from_dict(model['content'])
  notebook = _append_cell_contents(notebook)
  notebook_name = os.path.splitext(model.get('name', 'Notebook'))[0]
  # For some reason the from_notebook_node function does not bother to use the
  # notebook's metadata, so we need to extract it from the notebook, add it to
  # the resources dict, and pass it in directly.
  resources = nbconvert.exporters.exporter.ResourcesDict()
  resources['metadata'] = dict({'name': notebook_name}, **notebook['metadata'])

  (body, resources) = exporter.from_notebook_node(notebook, resources)

  return body


def _get_config(default=None):
    """Load and return the user's nbconvert configuration
    """
    config = Config(default) if default is not None else Config()
    app = NbConvertApp()
    app.load_config_file()
    _update_config(config, app.config)
    return config


def _update_config(a, b):
  """Updates a Config object with the values from a dict

  Unlike a normal dict update, this function will traverse through the nested
  structure of the original config object and if it finds a set or a sequence,
  it will update those with the values in the second dict; otherwise, it will
  overwrite the original value. This allows the function to preserve the
  original configuration settings while adding those from the second dict.

  """
  for k, v in b.items():
    if k in a:
      if isinstance(a[k], collections.Mapping):
        _update_config(a[k], v)
      elif isinstance(a[k], collections.Set):
        a[k] |= v
      elif isinstance(a[k], collections.MutableSequence):
        a[k].extend(v)
      else:
        a[k] = v
    else:
      a[k] = v


def _append_cell_contents(notebook):
  """Appends prior cell contents to a later cell dependent on labels

  This function will iterate through a notebook and grab all cells that have a
  label and add them to any cell that references that label (i.e., has the label
  in its ref_labels list). Each cell's content will be displayed according to
  the order of its appearance in the notebook.

  """
  Cell = collections.namedtuple('Cell', ['label', 'contents'])
  cells = []
  for cell in notebook['cells']:
    label = cell.get('metadata', {}).get('label', None)
    ref_labels = cell.get('metadata', {}).get('ref_labels', [])
    if label is not None:
      cells.append(Cell(label, cell['source']))
    elif ref_labels:
      cell['source'] = '\n\n'.join(cell.contents for cell in cells if cell.label in ref_labels).strip()

  return notebook
