import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


setup(name='candidate_estimator',
      version=0.1,
      description='REST API to estimate candidate',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
      ],
      keywords="web services",
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'cornice',
          'waitress',
          'sqlalchemy',
          'colander',
          'iso8601',
          'numpy',
          'pandas',
          'scipy',
          'scikit-learn',
      ],
      entry_points="""\
      [paste.app_factory]
      main=candidate_estimator:main
      """,
      paster_plugins=['pyramid'])
