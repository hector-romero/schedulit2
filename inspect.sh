#!/bin/bash

echo "### Executing flake8"
flake8

echo "### Executing pylint"
pylint schedulit

echo "### Executing mypy"
mypy schedulit
