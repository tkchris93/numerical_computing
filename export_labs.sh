#!/bin/bash
# Copy all files required to compile the tex files to a specified directory.

if ["$#" -ne 1 ]; then
    echo -e "Provide the name of the target directory"
else
    # Tex files
    find . -type f -name "*.tex" | cpio -pdv $1
    # Pictures and figures
    find . -type f -name "*.png" | cpio -pdv $1
    find . -type f -name "*.pdf" | cpio -pdv $1
    find . -type f -name "*.jpg" | cpio -pdv $1
    find . -type f -name "*.jpeg" | cpio -pdv $1
    # Support files
    cp SIAM-GH-book.cls $1
    find . -type f -depth 1 -name "*travis*" | cpio -pdv $1

    # Files included with \lstinputlisting[style=fromfile]{}
    mkdir $1/Appendices/f2py/flaplace
    mkdir $1/Appendices/f2py/fssor
    mkdir $1/Appendices/f2py/ftridiag

    cp Appendices/f2py/flaplace/flaplace.f90 $1/Appendices/f2py/flaplace
    cp Appendices/f2py/fssor/* $1/Appendices/f2py/fssor
    cp Appendices/f2py/ftridiag/* $1/Appendices/f2py/ftridiag
    cp Appendices/mpltables/*.py $1/Appendices/mpltables
    cp Vol1A/ImageSegmentation/getNeighbors.py $1/Vol1A/ImageSegmentation/getNeighbors.py
    cp Vol3B/WebTech1_InternetProtocol/tcp_server.py $1/Vol3B/WebTech1_InternetProtocol/tcp_server.py
    cp Vol3B/WebTech1_InternetProtocol/tcp_client.py $1/Vol3B/WebTech1_InternetProtocol/tcp_client.py
    cp Vol3B/WebTech2_Serialization/contacts.xml $1/Vol3B/WebTech2_Serialization/contacts.xml
    cp Vol4A/ShootingMethod/secant_method.py $1/Vol4A/ShootingMethod/secant_method.py

    # Remove extra files
    rm -rf $1/Orphans
    rm $1/InstructorNotes.tex
    rm $1/ExtraLabs.tex
    find $1 -type f -name "Notes.tex" -exec rm {} +
    if [ -e $1/onelab.tex ]; then
        rm $1/onelab.tex
    fi
fi
