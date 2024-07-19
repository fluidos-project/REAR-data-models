import argparse
import sys
import os
from plantuml import PlantUML

def write_text(data: str, path: str):
    with open(path, 'w') as file:
        file.write(data)

def generate_schema_svg(dir):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(script_dir, "..", "svg")

    plantuml = PlantUML(url='http://www.plantuml.com/plantuml/svg/')
    
    puml_files = [os.path.join(root, f) for root, _, files in os.walk(f"{dir}") for f in files if f.endswith(".puml")]
    
    for puml_file in puml_files:
        relative_path = os.path.relpath(puml_file, start=f"{dir}")
        svg_path = os.path.join(out_dir, relative_path).replace('.puml', '.svg')
        svg_dir = os.path.dirname(svg_path)
        if not os.path.exists(svg_dir):
            os.makedirs(svg_dir)
        plantuml.processes_file(puml_file, svg_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate SVG from PlantUML files')
    parser.add_argument('directory', type=str, help='The directory containing the PlantUML files')
    args = parser.parse_args()

    generate_schema_svg(args.directory)

