#!/bin/bash

while getopts v: flag
do
    case "${flag}" in
        v) version=${OPTARG};;
        a*)
    esac
done

echo "Version: $version"
echo "__version__ = \"$version\"" > src/defi_services/__init__.py

# Setup
python3 -m pip install build twine

# Run test
python3 -m pip install -r requirements.txt
python3 -m pip install pytest
pytest 2>&1 | tee tests/.log
status=${PIPESTATUS[0]}
if [ "$status" -ne 0 ]; then
    echo 'ERROR: pytest failed, exiting ...'
    exit "$status"
fi

# Clear dist
rm -rf dist/
echo "Clear dist"

# Build package
python3 -m build

# Confirm package build
twine check dist/*

# Upload package
#twine upload -r testpypi dist/*
twine upload dist/*
# Remove built package
rm -rf dist/