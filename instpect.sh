#!/bin/bash

flake8
pylint schedulit

mypy schedulit
