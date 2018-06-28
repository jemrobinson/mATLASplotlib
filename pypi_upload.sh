#! /bin/bash

# Create package
python setup.py sdist bdist_wheel

# Upload to pypi (use --repository-url https://test.pypi.org/legacy/ for testing)
twine upload dist/*

# Remove temporary files
rm -rf build/ dist/ mATLASplotlib.egg-info