from setuptools import setup, find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


def main():
    setup(
        name="pipeline_cv",
        version="0.0.0",
        install_requires=_requires_from_file('requirements.txt'),
        packages=find_packages(where='pipeline_cv'),
        package_dir={'': 'pipeline_cv'},
    )

if __name__ == "__main__":
    main()
