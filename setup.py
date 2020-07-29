import pathlib
from setuptools import setup

current_directory = pathlib.Path(__file__).parent
readme_file = (current_directory / "README.md").read_text()

setup(
    name="code2flow",
    version="1.1.0",
    description="A python module / CLI command to create flow charts from python code.",
    long_description=readme_file,
    long_description_content_type="text/markdown",
    url="https://github.com/Dheeraj1998/code2flow",
    author="Dheeraj Nair",
    author_email="nair.dheeraj@yahoo.co.in",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["code2flow"],
    include_package_data=True,
    install_requires=["graphviz"],
    entry_points={
        'console_scripts': [
            'code2flow = code2flow.__main__:main'
        ]
    }
)
