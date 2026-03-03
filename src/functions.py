from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		nodes_of_old = old_node.text.split(delimiter)
		if len(nodes_of_old) % 2 == 0:
			raise Exception(f"missing closing character: {delimiter}")
		temp_list = []
		for i in range(len(nodes_of_old)):
			if nodes_of_old[i] == "":
				continue
			if i % 2 == 0:
				temp_list.append(TextNode(nodes_of_old[i], TextType.TEXT))
			else:
				temp_list.append(TextNode(nodes_of_old[i], text_type))
		new_nodes.extend(temp_list)
	return new_nodes

def extract_markdown_images(text):
	matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def extract_markdown_links(text):
	matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def split_nodes_image(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		old_text = old_node.text
		matches = extract_markdown_images(old_text)
		if old_node.text_type != TextType.TEXT or matches == []:
			new_nodes.append(old_node)
			continue
		sections = []
		for match in matches:
			match_node = TextNode(match[0], TextType.IMAGE, match[1])
			sections = old_text.split(f"![{match[0]}]({match[1]})", 1)
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], TextType.TEXT))
			new_nodes.append(match_node)
			old_text = sections[1]
		if old_text != "":
			new_nodes.append(TextNode(old_text, TextType.TEXT))
	return new_nodes

def split_nodes_link(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		old_text = old_node.text
		matches = extract_markdown_links(old_text)
		if old_node.text_type != TextType.TEXT or matches == []:
			new_nodes.append(old_node)
			continue
		sections = []
		for match in matches:
			match_node = TextNode(match[0], TextType.LINK, match[1])
			sections = old_text.split(f"[{match[0]}]({match[1]})", 1)
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], TextType.TEXT))
			new_nodes.append(match_node)
			old_text = sections[1]
		if old_text != "":
			new_nodes.append(TextNode(old_text, TextType.TEXT))
	return new_nodes

def text_to_textnodes(text):
	# bold
	formatted = split_nodes_delimiter([TextNode(text, TextType.TEXT, None)], "**", TextType.BOLD)
	# italic
	formatted = split_nodes_delimiter(formatted, "_", TextType.ITALIC)
	# code
	formatted = split_nodes_delimiter(formatted, "`", TextType.CODE)
	# image
	formatted = split_nodes_image(formatted)
	# link
	formatted = split_nodes_link(formatted)
	
	return formatted

def markdown_to_blocks(markdown):
	separated = markdown.split("\n\n")
	blocks = []
	for item in separated:
		block = item.strip()
		if block != "":
			blocks.append(block)
	return blocks
			