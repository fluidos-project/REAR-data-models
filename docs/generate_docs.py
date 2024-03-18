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
example_dir = "models/examples/svg"

filenames = ["flavor.json", "flavor-types/k8slice.json", "flavor-types/service.json", "flavor-types/vm.json", "flavor-types/sensor.json"]
res = [""]
res.append("```")
res.append("DISCLAIMER #1: The content of this document is automatically generated upon pushing the files on GitHub. \nThe generation starts from the JSON schema and examples contained in the repository. \nDo not try to modify this document, just the JSON files.")
res.append("```")
res.append("```")
res.append("DISCLAIMER #2: Still, the generation of examples of JSONs (starting from the schema) is not automated yet. \nTherefore, we suggest to use tools like ChatGPT or Gemini, providing the JSON schema to the prompt and asking for an example of compliant JSON.")
res.append("```")
res.append("In the following we represent some examples of JSON, you can find the original JSON schemas [here](models/schemas).")

for id, f_name in enumerate(filenames):
    res.append("")
    if f_name == "flavor.json":
        res.append("# Flavor")
    else:
        res.append(f"## {f_name.replace('.json', '').replace('flavor-types/', '')}")
    
    res.append(f"![{str(id)}]({'/'.join([example_dir, f_name.replace('.json', '.svg')])})")
        
    f = open("/".join([dir, f_name]))
    data = json.load(f)

    generate_html(data["properties"], 0, res)
    
    if f_name == "flavor.json":
        res.append("")
        res.append("# FlavorType")
        res.append("The FlavorType describes the actual flavor that is adverised.")
        
text_file = open("../README.md", "w")
 
#write string to file
text_file.write("\n".join(res))
 
#close file
text_file.close()