#!/bin/bash

# Fix all files' permissions before pushing
sudo chmod 777 -R ./*
sudo chmod 777 -R .gitignore

# Give the commit a trivial name and push
git add .gitignore
# shellcheck disable=SC2035
git add *
git commit -m "Trivial update"
git push
