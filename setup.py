from distutils.core import setup

setup(
  name='jorts',
  version='0.1.0',
  author='Christopher Roach',
  author_email='christopher.g.roach@gmail.com',
  url='http://pypi.python.org/pypi/jorts/',
  packages=['jorts'],
  entry_points={
    'console_scripts': [
      'nb2pdf=jorts.cli:main'
    ]
  },
  include_package_data=True
)