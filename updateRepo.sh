#!/bin/bash

set -e                              # Exit as soon as one command fails.
git checkout develop
git pull upstream develop
git push origin develop

# Clean up the repository by removing auxiliary files.
set +e
find . -type f -name "*.pyc" -exec rm -f {} +
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
rm -f Vol?.[^tex]* Vol?.toc
rm -f ExtraLabs.[^tex]* ExtraLabs.toc
rm -f InstructorNotes.[^tex]* InstructorNotes.toc

git status
git branch
