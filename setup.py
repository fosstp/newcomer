import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_mailer',
    'pyramid_wtforms',
    'pyramid_tm',
    'pyramid_sqlalchemy',
    'pyramid_beaker',
    'alembic',
    'xlwt',
    'waitress',
    ]

setup(name='tp_enroll',
      version='0.0',
      description='tp_enroll',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="tp_enroll",
      entry_points="""\
      [paste.app_factory]
      main = tp_enroll:main
      """,
      )
