#!/bin/bash
# Copy all instructor materials to a specified directory.

if ["$#" -ne 1 ]; then
    echo -e "Provide the name of the target directory"
else
    # Solutions files (.py and .ipynb)
    find . -type f -name "solutions.py" | cpio -pdv $1
    find . -type f -name "solutions.ipynb" | cpio -pdv $1

    # Test drivers
    find . -type f -name "*test_driver*.py" | cpio -pdv $1

    # Auxiliary files
    cp -v Introduction/StandardLibrary/box.py $1/Introduction/StandardLibrary
    cp -v Vol1A/ImageSegmentation/getNeighbors.py $1/Vol1A/ImageSegmentation
    cp -v Vol1B/Testing/test_solutions.py $1/Vol1B/Testing
    cp -v Vol2B/ScipyOptimize/blackbox_function.py $1/Vol2B/ScipyOptimize
    cp -v Vol3B/WebTech1_IternetProtocol/*.py $1/Vol3B/WebTech1_IternetProtocol

    # Instructor notes
    find . -type f -name "*[Nn]otes.tex" | cpio -pdv $1
    cp -v SIAM-GH-book.cls $1
    cp -v command.tex $1
    cp -v Cover.pdf $1
    cp -v by.pdf $1

    # Remove extra directories
    rm -rf $1/Orphans
    rm -rf $1/Appendices
    rm -rf $1/MachineLearning
fi
