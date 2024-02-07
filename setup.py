from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sqli_finder_tool',
    version='4.0.10',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prasadd-1808/",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'sqli_finder_tool=sqli_finder_tool.main:main',
        ],
    },
)