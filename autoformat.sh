#! /bin/bash
echo "Running autopep8"
autopep8 mATLASplotlib --recursive --ignore=E501 --in-place

echo "Running pylint"
pylint mATLASplotlib