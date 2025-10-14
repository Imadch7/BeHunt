#!/bin/bash

current_dir=$(pwd)/"__init__.py"
echo "alias behunt='$current_dir'" >> ~/.zshrc 
source ~/.zshrc 
