#!/bin/bash

# Generate PlantUML diagram from schema files
# Usage: ./generate_puml.sh <directory>

# Check if directory parameter is provided
if [ -z "$1" ]; then
  echo "Usage: ./generate_puml.sh <directory>"
  exit 1
fi

# Store the directory path
directory="$1"

# Get the absolute path of the script in execution
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Create a new directory to store the PlantUML files
mkdir -p "$SCRIPT_DIR/../puml/$directory"

# Get the absolute path of the directory

# Open json schema files in the specified directory and generate PlantUML diagram
find "$directory" -type f -name "*.json" | while read -r filename; do
  new_filename=$(echo "$filename" | sed 's/\.schema\.json$//' | sed 's/\.json$//')
  # Create a new PlantUML file and its upper directory if necessary
  mkdir -p "$(dirname "$SCRIPT_DIR/../puml/$new_filename.puml")"
  # Add the PlantUML diagram header
  echo "@startjson" > "$SCRIPT_DIR/../puml/$new_filename.puml"
  # Add the content of the json schema file
  cat "$filename" >> "$SCRIPT_DIR/../puml/$new_filename.puml"
  # Add the PlantUML diagram footer
  echo "" >> "$SCRIPT_DIR/../puml/$new_filename.puml"
  echo "@endjson" >> "$SCRIPT_DIR/../puml/$new_filename.puml"
done
