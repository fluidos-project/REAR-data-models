import sys
import requests

def write_text(data: str, path: str):
    with open(path, 'w') as file:
        file.write(data)

def generate_schema_svg(dir, branch_name):
    out_dir = dir + "/svg"
    
    filenames = ["flavor.txt", "flavor-types/k8slice.txt", "flavor-types/service.txt", "flavor-types/vm.txt", "flavor-types/sensor.txt"]
    
    for f in filenames:
        response = requests.get(f"https://plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fluidos-project/REAR-data-models/{branch_name}/models/{dir}/puml/{f}&fmt=svg")
        write_text(response.text, f"{out_dir}/{f.replace('.txt', '.svg')}")

# get first CLI param 
branch = sys.argv[1]

generate_schema_svg("schemas", branch)
generate_schema_svg("examples", branch)
