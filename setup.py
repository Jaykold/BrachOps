from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='Jenkins-job',
    version='0.1',
    packages=find_packages(),
    author='Christian',
    install_requires=required
)