#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports mof

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place mof --exclude=__init__.py
black mof
isort mof
