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

# Clear dist
rm -rf dist/
echo "Clear dist"

# Build package
python3 -m build

# Confirm package build
twine check dist/*

# Upload package
twine upload -r testpypi dist/*
#twine upload dist/*
# Remove built package
rm -rf dist/