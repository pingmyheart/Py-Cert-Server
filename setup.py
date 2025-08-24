import warnings

from setuptools import setup, find_packages

# Suppress all warnings
warnings.filterwarnings("ignore")

setup(
    name='py-cert-server',
    version='0.0.6.dev0',
    packages=find_packages()
)
