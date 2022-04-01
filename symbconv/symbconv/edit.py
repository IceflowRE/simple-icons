import re
import traceback
import xml.etree.ElementTree as ET
from enum import Enum, auto
from pathlib import Path

from tqdm import tqdm


class EditActions(Enum):
    ADD_RECT = auto()
    CLEAN_UP = auto()  # removes not required inkscape entries
    MAKE_WHITE = auto()
    REMOVE_CIRCLE = auto()


def edit_svg_batch(paths: list[tuple[Path, Path]], actions: list[EditActions], desc: str) -> bool:
    """
    Edit svgs based on a path list.
    """
    success: bool = True
    for source, output in tqdm(paths, total=len(paths), desc=desc, unit='svg', mininterval=1, ncols=100, disable=False):
        try:
            edit_svg(source, output, actions)
        except Exception:
            success = False
            tqdm.write(f"Failed to apply changes to '{source}': {str(traceback.format_exc())}")
    return success


def edit_svg(source: Path, output: Path, actions: list[EditActions]):
    """
    Edit source svg and apply given actions and save to output.
    """
    # just be sure to not accidentally override the source file
    if source == output and actions != [EditActions.CLEAN_UP]:
        raise ValueError("source file cannot be the same as the output file.")

    def reg_namespace():
        ET.register_namespace("cc", "http://creativecommons.org/ns#")
        ET.register_namespace("dc", "http://purl.org/dc/elements/1.1/")
        ET.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
        ET.register_namespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        ET.register_namespace("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
        ET.register_namespace("svg", "http://www.w3.org/2000/svg")
        ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
        ET.register_namespace("", "http://www.w3.org/2000/svg")

    reg_namespace()
    tree = ET.parse(source)

    color = None
    if any(action in actions for action in [EditActions.MAKE_WHITE, EditActions.ADD_RECT]):
        color = get_color(tree)
        if color is None:
            raise Exception(f"{source} does not contain a circle")

    for action in actions:
        if action == EditActions.ADD_RECT:
            add_rounded_rect(tree, color)
        elif action == EditActions.CLEAN_UP:
            clean_up(tree)
        elif action == EditActions.MAKE_WHITE:
            make_colored(tree, color, "#ffffff")
        elif action == EditActions.REMOVE_CIRCLE:
            remove_circle(tree)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as writer:
        writer.write(b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        tree.write(writer, xml_declaration=False, method='xml', encoding='UTF-8')
        writer.write(b'\n')


RX_COLOR: re.Pattern = re.compile(r"stroke:(#[a-fA-F\d]{6})")


def get_color(tree: ET.ElementTree) -> str:
    """
    Get the color of the outer circle.
    """
    for child in tree.findall("{http://www.w3.org/2000/svg}circle"):
        if 'id' in child.attrib and 'style' in child.attrib and child.attrib['id'] and child.attrib['id'] == "circle":
            match = RX_COLOR.search(child.attrib['style'])
            if match is not None:
                return match.group(1)
    raise RuntimeError("Could not find color.")


def clean_up(tree: ET.ElementTree):
    root = tree.getroot()
    root.attrib.pop("{http://www.inkscape.org/namespaces/inkscape}version", None)
    root.attrib.pop("{http://www.inkscape.org/namespaces/inkscape}export-filename", None)
    root.attrib.pop("{http://www.inkscape.org/namespaces/inkscape}export-xdpi", None)
    root.attrib.pop("{http://www.inkscape.org/namespaces/inkscape}export-ydpi", None)
    root.attrib.pop("{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}docname", None)
    namedview = tree.find("{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview")
    if namedview is not None:
        root.remove(namedview)


def remove_circle(tree: ET.ElementTree):
    """
    Remove the circle.
    """
    root = tree.getroot()
    for child in tree.findall("{http://www.w3.org/2000/svg}circle"):
        if 'id' in child.attrib and child.attrib['id'] == "circle":
            root.remove(child)
            break


def add_rounded_rect(tree: ET.ElementTree, color: str):
    """
    Add a rounded rectangle.
    """
    root = tree.getroot()
    rect = ET.Element('rect')
    rect.attrib['id'] = "rect"
    rect.attrib['style'] = f"fill:none;stroke:{color};stroke-width:60;stroke-opacity:1;paint-order:fill markers stroke;stop-color:#000000"
    rect.attrib['width'] = "964"
    rect.attrib['height'] = "964"
    rect.attrib['x'] = "30"
    rect.attrib['y'] = "30"
    rect.attrib['rx'] = "192"
    rect.attrib['ry'] = "192"

    root.append(rect)


def make_colored(tree: ET.ElementTree, origin_color: str, new_color: str):
    """
    Makes the svg white.
    """
    for child in tree.iter():
        if 'style' in child.attrib:
            child.attrib['style'] = child.attrib['style'].replace(origin_color, new_color)
