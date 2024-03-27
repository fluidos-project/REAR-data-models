#!/bin/bash

# Generate PlantUML diagram from schema files
# Usage: ./generate_puml.sh

# Open json schema files and generate PlantUML diagram

# Flavor schema
echo "@startjson" > puml/flavor.txt
cat flavor.json >> puml/flavor.txt
echo "" >> puml/flavor.txt
echo "@endjson" >> puml/flavor.txt

for filename in $(ls flavor-types); do
  if test -f "flavor-types/$filename"; then
    new_filename=$(echo $filename | sed 's/.json//')
    echo "@startjson" > puml/flavor-types/$new_filename.txt
    cat flavor-types/$filename >> puml/flavor-types/$new_filename.txt
    echo "" >> puml/flavor-types/$new_filename.txt
    echo "@endjson" >> puml/flavor-types/$new_filename.txt
  fi
done