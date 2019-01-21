import os

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

    notebook = model['content']
    path = os.path.abspath(model['path'])
    root_dir = os.path.dirname(path)
    base, ext = os.path.splitext(os.path.basename(path))
    output_filename = "{}.pdf".format(base)

    convert_notebook_to_pdf(notebook, output_filename)

    handler.finish('Converted to {}!'.format(output_filename))