import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ahppy",
    description="A tool to model, build and evaluate AHP models",
    author="Iyed Ghedamsi",
    packages=find_packages(exclude=['data', 'figures', 'output', 'notebooks']),
    long_description=read('README.md'),
)
