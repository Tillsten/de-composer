#!/bin/bash

FILES=`find ./spec -name "*.py"`

for FILE in ${FILES[@]}; do
    $FILE
done
