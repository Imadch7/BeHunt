#!/bin/bash

current_dir=$(pwd)/"__init__.py"
echo "alias behunt='python3 $current_dir'" >> ~/.zshrc 
source ~/.zshrc 