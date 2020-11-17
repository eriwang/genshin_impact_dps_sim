#! /usr/bin/env bash

pylint src/
PYLINT_RC=$?

if [[ ($PYLINT_RC != 0) ]]; then
    echo "Found linting errors, see output for details" 1>&2
    exit 1
fi
