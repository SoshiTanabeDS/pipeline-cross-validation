from setuptools import setup


def _requires_from_file(filename):
    return open(filename).read().splitlines()


def main():
    setup(
        name="pipeline_cv",
        version="0.0.0",
        install_requires=_requires_from_file('requirements.txt')
    )

if __name__ == "__main__":
    main()
