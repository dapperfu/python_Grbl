#!/usr/bin/env bash

LEN=180

autopep8 --in-place --max-line-length ${LEN} --aggressive --aggressive --aggressive ${1}
black --target-version py37 --line-length=${LEN} ${1}
isort --line-width ${LEN} --multi-line 3 --dont-skip __init__.py ${1}
