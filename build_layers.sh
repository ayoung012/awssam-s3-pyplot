#!/bin/bash

# Loop through every directory in layers and produce a python directory
# to be copied into /opt of the server running our lambda function
PYTHON=python3

LAYERS_DIR=layers
REQ=requirements.txt


command -v $PYTHON >/dev/null 2>&1 || { echo >&2 "$PYTHON is required but it's not installed.  Aborting."; exit 1; }

for d in $(find $LAYERS_DIR -mindepth 1 -maxdepth 1 -type d); do
    echo "Building $d"

    # Dont skip, maybe requirements was updated

    # Skip if no requirements.txt
    [ -f $d/$REQ ] || { echo $d/$REQ missing, skipping; continue; }

    # Create a virtual env for our layer packages
    if [ -d "$d/python" ]; then
        echo Virtual env already exists
    else
        echo Creating virtual env
        python3 -m venv "${d}/python"
    fi

    # Activate the virtual env and install requirements.txt
    source $d/python/bin/activate
    $PYTHON -m pip install --no-deps -r $d/$REQ
    deactivate

    # Delete the lib64 symlink if it exists
    # This doubles the size of the layer thanks to the native python zip library
    # https://github.com/awslabs/aws-sam-cli/issues/477
    # https://github.com/brefphp/bref/issues/146

    if [ -L "$d/python/lib64" ]; then
        rm -f $d/python/lib64
    fi

    echo
    echo
    
done

exit 0

which python3
python3 -m pip install numpy
