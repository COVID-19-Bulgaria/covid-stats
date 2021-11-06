'''
covid-stats: Charts and visualisations for the COVID-19 spread in Bulgaria

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2021, Veselin Stoyanov.
Licensed under Attribution-NonCommercial-ShareAlike 4.0 International.
'''
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


version = "1.12"

setup(name="covid-stats",
      version=version,
      description="Charts and visualisations for the COVID-19 spread in Bulgaria",
      long_description=open("README.rst").read(),
      classifiers=[  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 1 - Planning',
          'Programming Language :: Python'
      ],
      keywords="covid,covid-19,coronavirus,sars-cov-2,Bulgaria",  # Separate with spaces
      author="Veselin Stoyanov",
      author_email="me@vesko.dev",
      url="https://coronavirus-bulgaria.org",
      license="Attribution-NonCommercial-ShareAlike 4.0 International",
      packages=find_packages(exclude=['examples', 'tests']),
      package_data={'covidstats': ['config/**/*']},
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest'],
      cmdclass={'test': PyTest},

      # TODO: List of packages that this one depends upon:   
      install_requires=[
          'numpy',
          'pandas',
          'matplotlib',
          'seaborn',
          'pydlm',
          'epyestim',
          'python-i18n[YAML]'
      ],
      # TODO: List executable scripts, provided by the package (this is just an example)
      entry_points={
          'console_scripts':
              ['covid_stats=covidstats:main']
      }
      )
