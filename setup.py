"""
    Setup script for distribution.
"""
import os
import os.path as op
import textwrap
import fnmatch
from collections import defaultdict

from setuptools import find_packages, setup

# Try to fetch settings from the environment.
VERSION = os.environ.get('VERSION')
RUNTIME_DEPS = os.environ.get('RUNTIME_DEPS', '').split()
VERSION_FILE_PATH = op.join(
    op.dirname(__file__), 'pipeline_cv', '_version.py')

# VERSION not defined: may be running in the build system, so scrape the
# _version.py file.  We don't care about RUNTIME_DEPS, since those are
# explicitly added by the recipe.
if VERSION is None:

    # Running in build context from source tarball
    if op.exists(VERSION_FILE_PATH):
        with open(VERSION_FILE_PATH, 'r') as fp:
            code = compile(fp.read(), 'pipeline_cv._version',
                           'exec')
        context = {}
        exec(code, context)
        VERSION = context['version']

    # Running from a clean git checkout
    else:
        VERSION = '0.0.0'


def main():
    """ Entry point for script execution. """

    with open(VERSION_FILE_PATH, 'w') as f:
        f.write(
            textwrap.dedent("""\
            # THIS FILE IS GENERATED FROM SETUP.PY
            version = '{version}'
            """.format(version=VERSION)))

    def find_package_data():

        package_data = defaultdict(list)

        for root, dirnames, filenames in os.walk('pipeline_cv'):
            for ext in ['*.png', '*.ico']:
                if fnmatch.filter(filenames, ext):
                    package_data[root.replace(os.sep, '.')].append(ext)

        return dict(package_data)

    setup(
        name='pipeline_cv',
        version=VERSION,
        license='Proprietary',
        packages=find_packages(include=[
            'pipeline_cv', 'pipeline_cv.*'
        ]),
        install_requires=RUNTIME_DEPS,
        package_data=find_package_data(),
    )


if __name__ == '__main__':
    main()
