import json
import os
import argparse

def generate_html(data, base_dir, depth, res):
    spaces = "  " * depth
    
    for key, value in data.items():
        if "oneOf" in value:
            res.append(f"{spaces}- **{key}**. {value['description']}")
            continue
        if "$ref" in value:
            ref = value["$ref"]
            if ref.startswith("http"):
                res.append(f"{spaces}- **{key}**. {value.get('description', '')} [Reference: {ref}]")
            else:
                ref_name = os.path.basename(ref).replace('.schema.json', '')
                res.append(f"{spaces}- **{key}**. {value.get('description', '')} [Reference: #{ref_name}]")
        elif value["type"] != "object":
            res.append(f"{spaces}- **{key}**. {value.get('description', '')} [{value['type']}]")
        else:
            res.append(f"{spaces}- **{key}**:")
            generate_html(value["properties"], base_dir, depth + 1, res)

def generate_type_markdown(type_name, type_data, schema_name, docs_base_dir, schema_svg_dir, example_svg_dir, relative_path):
    lines = [f"# {type_name.capitalize()}"]
    lines.append("")
    
    schema_svg_path = os.path.abspath(os.path.join(schema_svg_dir, relative_path, f"{type_name}.svg"))
    example_svg_path = os.path.abspath(os.path.join(example_svg_dir, relative_path, f"{type_name}.svg"))
    schema_svg_relative_path = os.path.relpath(schema_svg_path, os.path.join(docs_base_dir, relative_path))
    example_svg_relative_path = os.path.relpath(example_svg_path, os.path.join(docs_base_dir, relative_path))
    
    lines.append(f"![Example SVG]({example_svg_relative_path})")
    lines.append("")
    lines.append(f"[Show schema SVG]({schema_svg_relative_path})")
    lines.append("")
    
    generate_html(type_data["properties"], docs_base_dir, 0, lines)
    type_md_path = os.path.join(docs_base_dir, relative_path, f"{type_name}.md")
    os.makedirs(os.path.dirname(type_md_path), exist_ok=True)
    
    with open(type_md_path, "w") as type_md_file:
        type_md_file.write("\n".join(lines))

def process_directory(base_dir, schema_svg_dir, example_svg_dir, res, depth=0):
    docs_base_dir = os.path.join(os.getcwd(), 'docs')

    # Create array of subdirectories already mapped as related components
    subdirs = []
    
    for root, dirs, files in os.walk(base_dir):

        print(f"Processing {root}")
        print(f"dirs: {dirs}")
        print(f"files: {files}")

        if root in subdirs:
            continue

        schema_files = [f for f in files if f.endswith(".schema.json")]
        if not schema_files:
            continue
        
        relative_path = os.path.relpath(root, base_dir)        

        for f_name in schema_files:
            schema_name = f_name.replace('.schema.json', '')
            schema_path = os.path.join(root, f_name)

            # Calculate SVG paths
            schema_svg_path = os.path.abspath(os.path.join(schema_svg_dir, relative_path, f"{schema_name}.svg"))
            example_svg_path = os.path.abspath(os.path.join(example_svg_dir, relative_path, f"{schema_name}.svg"))
            schema_svg_relative_path = os.path.relpath(schema_svg_path, os.getcwd())
            example_svg_relative_path = os.path.relpath(example_svg_path, os.getcwd())

            res.append("")
            res.append(f"{'#' * (depth + 2)} {schema_name.capitalize()}")       
            res.append("")     
            res.append(f"![Example SVG]({example_svg_relative_path})")
            res.append("")
            res.append(f"[Show schema SVG]({schema_svg_relative_path})")
            res.append("")   
            
            with open(schema_path) as f:
                data = json.load(f)

            generate_html(data["properties"], root, depth + 1, res)

            # Check for subdirectory types but do not process them here
            types_dir = os.path.join(root, f"{schema_name}-types")
            if os.path.isdir(types_dir):
                # Add directory to array
                subdirs.append(types_dir)
                res.append(f"### {schema_name.capitalize()} types")
                type_files = [f for f in os.listdir(types_dir) if f.endswith('.schema.json')]
                for type_file in type_files:
                    type_name = type_file.replace('.schema.json', '')
                    type_md_relative_path = os.path.relpath(
                        os.path.join('docs', f"{schema_name}-types", f"{type_name}.md"), os.getcwd()
                    )
                    res.append(f"- [{type_name.capitalize()}]({type_md_relative_path})")
                    with open(os.path.join(types_dir, type_file)) as tf:
                        type_data = json.load(tf)
                    generate_type_markdown(type_name, type_data, schema_name, docs_base_dir, schema_svg_dir, example_svg_dir, os.path.join(relative_path, f"{schema_name}-types"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate README.md from JSON schemas.')
    parser.add_argument('schema_dir', type=str, help='The directory containing the JSON schemas')
    parser.add_argument('schema_svg_dir', type=str, help='The directory containing the schema SVGs')
    parser.add_argument('example_svg_dir', type=str, help='The directory containing the example SVGs')
    args = parser.parse_args()
    
    res = [""]
    res.append("```")
    res.append("DISCLAIMER #1: The content of this document is automatically generated upon pushing the files on GitHub. \nThe generation starts from the JSON schema and examples contained in the repository. \nDo not try to modify this document, just the JSON files.")
    res.append("```")
    res.append("```")
    res.append("DISCLAIMER #2: Still, the generation of examples of JSONs (starting from the schema) is not automated yet. \nTherefore, we suggest to use tools like ChatGPT or Gemini, providing the JSON schema to the prompt and asking for an example of compliant JSON.")
    res.append("```")
    res.append("In the following we represent some examples of JSON, you can find the original JSON schemas [here](models/schemas).")

    process_directory(args.schema_dir, args.schema_svg_dir, args.example_svg_dir, res)

    with open("README.md", "w") as text_file:
        text_file.write("\n".join(res))
