def extract_title(markdown):
	lines = markdown.splitlines()
	for line in lines:
		if line.startswith("# "):
			main_heading = line.removeprefix("# ").strip()
			return main_heading
	raise Exception("no h1 found")