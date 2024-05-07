#!/bin/bash

# Define source and target directories
src_dir="GridboxConnectorAddon-dev"
target_dir="GridboxConnectorAddon"

# Copy all files from source to target directory, excluding config.yml and build.yml
rsync -av --exclude='config.yml' --exclude='build.yml' $src_dir/ $target_dir/