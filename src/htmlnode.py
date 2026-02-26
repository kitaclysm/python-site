class HTMLNode():
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError()
  
  def props_to_html(self):
    if self.props is None or self.props == "":
      return ""
    formatted = ""
    for item in self.props:
      formatted += f" {item}=\"{self.props[item]}\""
    return formatted
  
  def __repr__(self):
    return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
  
class LeafNode(HTMLNode):
  def __init__(self, tag, value, props = None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      raise ValueError("no value")
    if self.tag is None:
      return self.value
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
  
  def __repr__(self):
    return f"Tag: {self.tag}, Value: {self.value}, Props: {self.props}"
  
class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag=tag, value=None, children=children, props=props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("no tag")
    if self.children is None:
      raise ValueError("no children")
    html_string = f"<{self.tag}{self.props_to_html()}>"
    for child in self.children:
      html_string += child.to_html()
    html_string += f"</{self.tag}>"
    return html_string