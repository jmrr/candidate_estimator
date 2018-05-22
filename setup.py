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
          'cornice==3.4.0',
          'waitress==1.1.0',
          'sqlalchemy==1.2.7',
          'colander==1.4',
          'iso8601==0.1.12',
          'numpy==1.14.3',
          'pandas==0.23.0',
          'scipy==1.1.0',
          'scikit-learn==0.19.1',
      ],
      entry_points="""\
      [paste.app_factory]
      main=candidate_estimator:main
      """,
      paster_plugins=['pyramid'])
