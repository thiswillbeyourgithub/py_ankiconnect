
from setuptools import setup, find_packages
from setuptools.command.install import install

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="{project_name}",
    version="0.0.1",
    description="TODO_description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="TODO_URL",
    packages=find_packages(),

    # TODO_check_values
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GPLv3",
    keywords=["TODO_keywords"],
    python_requires=">=3.11",

    entry_points={
        'console_scripts': [
            '{project_name}={project_name}.__init__:cli_launcher',
        ],
    },

    install_requires=[
        "fire >= 0.6.0",
        "beartype >= 0.18.5",
        # TODO_req
    ],
    extra_require={
    'optionnal_feature': [
        # TODO_req
        ]
    },

)
