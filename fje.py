import json
import argparse
from Visitor import *

class JSONComponent(ABC):
    def __init__(self):
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    @abstractmethod
    def accept(self, visitor, indent="", is_last=True, is_root=True, total=7):
        pass

    def __iter__(self):
        return JSONIterator(self)


class JSONObject(JSONComponent):
    def __init__(self, name, icon=0, position=0):
        super().__init__()
        self.name = name
        self.icon = icon_family[icon][0]
        self.position = position

    def accept(self, visitor, indent="", is_last=True, is_root=True, total=7):
        return visitor.visitContainer(self, indent, is_last, is_root, total)


class JSONLeaf(JSONComponent):
    def __init__(self, name, value=None, icon=0, position=0):
        super().__init__()
        self.name = name
        self.value = value
        self.icon = icon_family[icon][1]
        self.position = position

    def accept(self, visitor, indent="", is_last=True, is_root=False, total=7):
        return visitor.visitLeaf(self, indent, is_last, is_root, total)

    def __iter__(self):
        return iter([])  # Leaves have no children


class Iterator:
    def __init__(self):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass



class JSONIterator(Iterator):
    def __init__(self, root):
        self.stack = [(root, -1)]  # Stack holds tuples of (component, child_index)

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            component, child_index = self.stack.pop()
            if child_index == -1:  # New component
                self.stack.append((component, 0))
                return component
            elif child_index < len(component.children):
                self.stack.append((component, child_index + 1))
                child = component.children[child_index]
                self.stack.append((child, -1))
                return child
        raise StopIteration




def count_nodes(data):
    if isinstance(data, dict):
        count = 1
        for value in data.values():
            count += count_nodes(value)
        return count
    elif isinstance(data, list):
        count = 1
        for item in data:
            count += count_nodes(item)
        return count
    else:
        return 1


def build_tree(json_data, icon):
    node_counter = [1]  # Using a list to act as a mutable integer to keep track of positions

    def build_node(name, data, position=1):
        if isinstance(data, dict):
            node = JSONObject(name=name, icon=icon, position=position)
            for key, value in data.items():
                child_position = node_counter[0]
                node_counter[0] += 1
                if isinstance(value, (dict, list)):
                    child = build_node(str(key), value, child_position)
                    node.add_child(child)
                else:
                    leaf = JSONLeaf(name=str(key), value=str(value), icon=icon, position=child_position)
                    node.add_child(leaf)
            return node
        elif isinstance(data, list):
            node = JSONObject(name=name,  icon=icon, position=position)
            for i, item in enumerate(data):
                child_position = node_counter[0]
                node_counter[0] += 1
                if isinstance(item, (dict, list)):
                    child = build_node(str(i), item, child_position)
                    node.add_child(child)
                else:
                    leaf = JSONLeaf(name=str(i), value=str(item),  icon=icon, position=child_position)
                    node.add_child(leaf)
            return node
        else:
            return JSONLeaf(name=name, value=str(data),  icon=icon, position=position)

    total_nodes = count_nodes(json_data)
    root_node = build_node("root", json_data)
    return root_node


# Main Function
def main():
    print("21307296 薛锦俊")
    parser = argparse.ArgumentParser(description='Funny JSON Explorer (FJE)')
    parser.add_argument('-f', '--file', required=True, help='JSON file to visualize')
    parser.add_argument('-s', '--style', choices=['tree', 'rectangle'], required=True, help='Visualization style')
    parser.add_argument('-i', '--icon', choices=list(map(str, range(len(icon_family)))), required=True,
                        help='Icon set to use')
    args = parser.parse_args()

    with open(args.file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    if args.style == 'tree':
        visitor = TreeVisitor()
    elif args.style == 'rectangle':
        visitor = RectangleVisitor()

    # 构建树形结构
    root_component = build_tree(json_data, int(args.icon))
    # 对根组件调用 accept 方法并传递访问者对象
    result = root_component.accept(visitor)
    print(result)


if __name__ == "__main__":
    main()
