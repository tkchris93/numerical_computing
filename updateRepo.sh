#!/bin/bash

set -e                              # Exit as soon as one command fails.

git checkout develop
git pull upstream develop
git push origin develop
git status
git branch
