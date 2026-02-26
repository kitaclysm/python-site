from textnode import TextNode, TextType

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
