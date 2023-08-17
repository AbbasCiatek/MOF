#!/bin/sh -ex

mypy mof
flake8 mof
black mof --check
isort mof --check-only
