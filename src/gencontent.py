import os

from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
	lines = markdown.splitlines()
	for line in lines:
		if line.startswith("# "):
			main_heading = line.removeprefix("# ").strip()
			return main_heading
	raise Exception("no h1 found")

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_content = f.read()
    with open(template_path) as g:
        template_content = g.read()
    content = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", content)
    template_content = template_content.replace("href=\"/", f"href=\"{base_path}")
    template_content = template_content.replace("src=\"/", f"src=\"{base_path}")
    if os.path.dirname(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as h:
        h.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    files = os.listdir(dir_path_content)
    for item in files:
        itempath = os.path.join(dir_path_content, item)
        destpath = os.path.join(dest_dir_path, item)
        if os.path.isfile(itempath) and itempath.endswith(".md"):
            destpath = destpath.replace(".md", ".html")
            generate_page(itempath, template_path, destpath, base_path)
        else:
            generate_pages_recursive(itempath, template_path, destpath, base_path)