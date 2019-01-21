import io
import os

import nbformat

from .converter import convert_notebook_to_pdf

def _jupyter_bundlerextension_paths():
    """Example "hello world" bundler extension"""
    return [{
        'name': 'jorts_bundler',
        'label': 'Human Readable Report (.pdf)',
        'module_name': 'jorts',
        'group': 'download'
    }]


def bundle(handler, model):
    """Transform, convert, bundle, etc. the notebook referenced by the given
    model.

    Then issue a Tornado web response using the `handler` to redirect
    the user's browser, download a file, show a HTML page, etc. This function
    must finish the handler response before returning either explicitly or by
    raising an exception.

    Parameters
    ----------
    handler : tornado.web.RequestHandler
        Handler that serviced the bundle request
    model : dict
        Notebook model from the configured ContentManager
    """

    notebook_filename = model['name']
    notebook_content = nbformat.writes(model['content']).encode('utf-8')
    notebook_content = model['content']
    import pdb; pdb.set_trace()

    notebook_name = os.path.splitext(notebook_filename)[0]
    # If the notebook doesn't have a name (which will be the report's title),
    # grabe the file name and use that as the title.
    if 'name' not in notebook_content['metadata']:
      notebook_content['metadata']['name'] = notebook_name
    pdf_filename = '{}.pdf'.format(notebook_name)

    with io.BytesIO() as pdf_buffer:
      pdf_body = convert_notebook_to_pdf(notebook_content)
      pdf_buffer.write(pdf_body)

      handler.set_attachment_header(pdf_filename)
      handler.set_header('Content-Type', 'application/pdf')

      # Return the buffer value as the response
      handler.finish(pdf_buffer.getvalue())
