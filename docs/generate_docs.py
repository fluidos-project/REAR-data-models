import json

def generate_html(data, depth, res):
    spaces = ""
    for i in range(depth):
        spaces += " "
        spaces += " "
        
    for key in data:
        if "oneOf" in data[key]:
            res.append(f"{spaces}- **{key}**. {data[key]['description']}")
            continue
        if data[key]["type"] != "object":
            res.append(f"{spaces}- **{key}**. {data[key]['description']} {[data[key]['type']]}")
        else:
            res.append(f"{spaces}- **{key}**:")
            generate_html(data[key]["properties"], depth + 1, res)

dir = "../models/schemas"
example_dir = "../models/examples/svg"

filenames = ["flavor.json", "flavor-types/k8slice.json", "flavor-types/service.json", "flavor-types/vm.json", "flavor-types/sensor.json"]
res = [""]

for id, f_name in enumerate(filenames):
    if f_name == "flavor.json":
        res.append("# Flavor")
    else:
        res.append(f"## {f_name.replace('.json', '').replace('flavor-types/', '')}")
    
    res.append(f"![{str(id)}]({'/'.join([example_dir, f_name.replace('.json', '.svg')])})")
        
    f = open("/".join([dir, f_name]))
    data = json.load(f)

    generate_html(data["properties"], 0, res)
    
    if f_name == "flavor.json":
        res.append("# FlavorType")
        res.append("The FlavorType describes the actual flavor that is adverised.")
        
text_file = open("README.md", "w")
 
#write string to file
text_file.write("\n".join(res))
 
#close file
text_file.close()