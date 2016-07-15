#!/bin/bash

set -e                              # Exit as soon as one command fails.

if [ "$#" -ne 1 ]; then             # Check for a command line argument.
    echo -e "Provide the name of the branch to be deleted"
else                                # Delete the specified git branch.
    echo -e "\nAttempting to delete branch $1...\n"
    git checkout develop
    git pull upstream develop
    git push origin develop
    git checkout $1
    git merge develop
    git checkout develop
    git branch -d $1
    git push origin :$1
    echo -e "\nDone\n"
    git branch
    git status
fi
