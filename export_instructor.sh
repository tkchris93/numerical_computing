#!/bin/bash
# Copy all instructor materials to a specified directory.

if ["$#" -ne 1 ]; then
    echo -e "Provide the name of the target directory"
else
    # Solutions files (.py and .ipynb)
    find . -type f -name "solutions.py" | cpio -pdv $1
    find . -type f -name "solutions.ipynb" | cpio -pdv $1
    # Test drivers TODO: "*test_driver*.py"
    find . -type f -name "testDriver.py" | cpio -pdv $1
    # Instructor Notes
    find . -type f -name "*[Nn]otes.tex" | cpio -pdv $1
    cp SIAM-GH-book.cls $1
    cp command.tex $1
    cp *.pdf $1
fi