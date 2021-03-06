# Jorts (Jupyter repORTS)

A bundler extension for exporting notebooks to human readable PDFs

Though Jupyter notebooks are fantastic for performing ad-hoc analyses and making
research repeatable, they're not a particularly great format for sharing results
with decision makers who may not have the technical expertise to run a Jupyter
notebook and/or understand the code. This Jupyter [bundler
extension][bundlerextension] provides a download option that creates reports
without all the unnecessary code, intermediate output, etc. that may muddy the
report's central message.

[bundlerextension]: https://jupyter-notebook.readthedocs.io/en/stable/extending/bundler_extensions.html#custom-bundler-extensions

## Installation

To install the Jorts bundler extension, follow the steps below.

1. Clone the repository

```
git clone https://github.com/croach/jorts.git
```

2. `cd` into the repository's root directory

```
cd jorts
```

3. Install the package

```
pip install jorts
```

4. Enable the extension (optional)

```
jupyter bundlerextension enable --py jorts --sys-prefix
```

Technically, the final step is optional since you don't need to enable the
bundler extension to use this package to create good looking reports. The jorts
package also provides a commmand line interface called `nb2pdf`, which is
explained in the next section. However, to have the ability to export to PDF via
menu item within a Jupyter notebook, you must enable the extension by running
the command in step 3 above.

## Usage

To accomplish more complex tasks, such as hiding the input and/or output of a
specific cell, you just need to update that cell's metadata. To edit a cell's
metadata, you must first reveal the "Edit Metadata" buttons on each cell by
selecting View > Cell Toolbar > Edit Metadata in the Jupyter notebook window.
Then, simply click on a cell's "Edit Metadata" button and modify the metadata
for that cell. As an example, let's assume that I have a bit of code that
creates a histogram of some data I'm investigating and I want the visualization
to show up in the report, but the code it not needed. In this specific case I
would want to hide the input (i.e., the code), but still show the generated
visualization. To do so, I would simply add the "hide_input" tag to the cell's
metadata, like so.

```json
{
  "tags": [
    "hide_input"
  ]
}
```

The `jupyter_nbconvert_config.py` file contains the configuration for the
nbconvert command and you'll find the tag that you just used in the example
above defined in this file. In this file there are three tags defined in total:
hide_input, hide_output, and hide_all.

Even more interesting is the ability to move all of the code within a notebook
to an appendix. Doing so keeps the report itself very clean, while still
including the code for the reader's review.

### Moving Code to an Appendix

To use the appendix feature, just add a "label" to any cell's metadata, and then
reference that label in the "ref_labels" list of the metadata of the cell where
you want to display the contents later in the notebook. To also hide the
contents of the cell inline, add a "hide_all" tag to its metadata. An example of
the metadata for a cell that both adds a label (for later reference) and hides
the contents of the cell inline can be seen below.

```json
{
  "tags": [
    "hide_all"
  ],
  "label": "appendix"
}
```

To display the cell's contents in an appendix, simply add a cell later in the
notebook where you want the code to be displayed and add the labels of the cells
that you want to display in the "ref_labels" list. An example of the metadata of
a cell that displays the labeled cell's contents is given below.

```json
{
  "ref_labels": [
    "appendix"
  ]
}
```

The labeled cell's contents will be stitched together in order of their
appearance in the document.


## The Command Line Interface

To generate PDF-based reports from the command line, just run the `nb2pdf`
command (as the example below shows) to convert your notebook to a PDF complete
with handy defaults that make the resultant report much more readable than what
can be generated by the default PDF export option(s).

```
nb2pdb notebook_name.ipynb --output output.pdf
```

## Auto-Generating Reports

As described above, you can generate a PDF report by running the `nb2pdf` script
at the command line. However, this may seem a tad cumbersome to use when you
want to generate a new report every time you update your notebook. A more
elegant and easy way to generate your reports automatically, would be to take
advantage of a post save script that will generate the report every time the
notebook is saved. This feature is turned off by default, so you must explicitly
turn it on to take advantage of it. To turn this feature on, open the
`jupyter_notebook_config.py` file and uncomment the last line in the file (which
I've listed below to make it easier to find). Once you've uncommented that line,
just kill and restart your notebook and the next time you save the notebook
file, you should see a new file generated for you with the notebook file's name
and the .pdf extension.

```python
#c.FileContentsManager.post_save_hook = script_post_save
```
