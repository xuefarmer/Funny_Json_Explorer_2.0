from config import icon_family
from abc import ABC, abstractmethod
class Visitor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def visitContainer(self, component, indent: str = "", is_last: bool = False, is_root: bool = False, total: int = 1,
                       line_length: int = 100) -> str:
        pass

    @abstractmethod
    def visitLeaf(self, component, indent: str = "", is_last: bool = False, is_root: bool = False, total: int = 1,
                  line_length: int = 100) -> str:
        pass


class TreeVisitor(Visitor):
    def visitContainer(self, component, indent: str, is_last: bool, is_root: bool, total: int,
                       line_length: int = 100) -> str:
        if is_root:
            result = ""
        else:
            line_prefix = "└─ " if is_last else "├─ "
            result = f"{indent}{line_prefix}{component.icon}{component.name}\n"

        for i, child in enumerate(component):
            label = "   " if is_last else "│  "
            if is_root:
                label = ""
            result += child.accept(self, indent + label, i == len(component.children) - 1, False, total)
        return result

    def visitLeaf(self, component, indent: str, is_last: bool, is_root: bool, total: int,
                  line_length: int = 100) -> str:
        if component.value is None:
            return ""


        line_prefix = "└─ " if is_last else "├─ "

        if component.value =="None":
            return f"{indent}{line_prefix}{component.icon}{component.name}\n"
        return f"{indent}{line_prefix}{component.icon}{component.name}: {component.value}\n"


class RectangleVisitor(Visitor):
    def visitContainer(self, component, indent: str, is_last: bool, is_root: bool, total: int,
                       line_length: int = 100) -> str:
        if is_root:
            result = ""
        else:
            if component.position == total:
                line_prefix = "└─"
            elif component.position == 1:
                line_prefix = "┌─ "
            else:
                line_prefix = "├─ "
            line_content = f"{indent}{line_prefix}{component.icon}{component.name}"
            padding = line_length - len(line_content) - 2  # Account for the '┐' or '┤'
            if component.position == 1:
                result = f"{line_content} {'─' * padding}┐\n"
            else:
                result = f"{line_content} {'─' * padding}┤\n"

        for i, child in enumerate(component):
            label = "│  "
            if is_root:
                label = ""
            if component.position + i + 1 == total:
                label = "└─ "
            result += child.accept(self, indent + label, i == len(component.children) - 1, False, total)
        return result

    def visitLeaf(self, component, indent: str, is_last: bool, is_root: bool, total: int,
                  line_length: int = 100) -> str:
        if component.value is None:
            return ""

        if component.position == total:
            line_prefix = "└─ "
        elif component.position == 1:
            line_prefix = "┌─ "
        else:
            line_prefix = "├─ "
        line_content = f"{indent}{line_prefix}{component.icon}{component.name}"
        if component.value != "None":
            line_content += f": {component.value}"
        padding = line_length - len(line_content) - 2  # Account for the '┤'
        if component.position == 1:
            result = f"{line_content} {'─' * padding}┐\n"
        elif component.position == total:
            result = f"{line_content} {'─' * padding}┘\n"
        else:
            result = f"{line_content} {'─' * padding}┤\n"
        return result
