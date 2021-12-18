import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='afterpay',
    version='0.2.0',
    author="nyneava",
    author_email="",
    description="Python library for interacting with Afterpay API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nyneava/afterpay-python",
    packages=setuptools.find_packages(),
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ],
)