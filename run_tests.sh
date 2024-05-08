#!/bin/sh

python -m black --line-length=120 --check .
export black_result=$?
if [ $black_result -ne 0 ]; then
  echo "Please run black to format files."
  exit 1
fi

python -m flake8 --max-line-length=200 --ignore=E722,W503,E203 --exclude=venv,venv_old,node_modules
export flake8_result=$?
if [ $flake8_result -ne 0 ]; then
  echo "flake8 failed with exit code: " $flake8_result
  exit 1
fi

python -m pytest --junitxml=reports/unit_tests.xml
export test_result=$?
python -m coverage xml -o reports/coverage.xml
if [ $test_result -ne 0 ]; then
  echo "Tests failed with exit code: " $test_result
  exit 1
fi

## TODO to be enabled
# python -m coverage report -m --fail-under=90
