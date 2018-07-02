from setuptools import find_packages, setup

with open("README.md", "r") as f_readme:
    long_description = f_readme.read()

setup(
    name                          = "mATLASplotlib",
    version                       = "1.0",
    description                   = "Wrappers around matplotlib functionality to produce plots compatible with the style guidelines for the ATLAS experiment at the LHC",
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/jemrobinson/mATLASplotlib",
    author                        = "James Robinson",
    author_email                  = "james.em.robinson@gmail.com",
    license                       = "GPLv3",
    install_requires              = ["matplotlib", "numpy", "scipy"],
    packages                      = find_packages(),
)