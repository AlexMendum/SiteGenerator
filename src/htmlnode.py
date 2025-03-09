class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        formatted_list = []
        for key, value in self.props.items():
            formatted_pair =  f' {key}="{value}"'
            formatted_list.append(formatted_pair)
        return "".join(formatted_list)
    
    def __repr__(self):
        children_string = "None" if self.children is None else str(self.children)
        props_string = "None" if self.props is None else str(self.props)
        return f"tag: {self.tag}, value: {self.value}, children: {children_string}, props: {props_string}"
        

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children is None:
            raise ValueError("children has no value")
        html_string = f"<{self.tag}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    


