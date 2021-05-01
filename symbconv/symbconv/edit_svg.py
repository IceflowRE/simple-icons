import multiprocessing
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum, auto
from pathlib import Path
from lxml import etree
from tqdm import tqdm


class EditActions(Enum):
    REMOVE_CIRCLE = auto()
    ADD_RECT = auto()
    MAKE_WHITE = auto()


def edit_svg_entry(paths: list[tuple[Path, Path]], actions: list[EditActions]) -> bool:
    job_list = []
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        for source, output in paths:
            job = executor.submit(edit_svg, source, output, actions)
            job_list.append(job)

        pbar = tqdm(as_completed(job_list), total=len(job_list), desc="applying changes", unit='svg', mininterval=1, ncols=100, disable=False)
        for _ in pbar:
            pass

    success = True
    for job in job_list:
        try:
            job.result()
        except Exception as ex:
            tqdm.write(f"Failed to apply changes to a file: {str(ex)}")
            success = False
    return success


def edit_svg(source: Path, output: Path, actions: list[EditActions]):
    """
    Edit source svg and apply given actions and save to output.
    """
    # just be sure to not accidentally override the source file
    if source == output:
        raise ValueError("source file cannot be the same as the output file.")

    tree = etree.parse(str(source))

    color = get_color(tree)
    if color is None:
        raise Exception(f"{source} does not contains a circle")

    for action in actions:
        if action == EditActions.REMOVE_CIRCLE:
            remove_circle(tree)
        elif action == EditActions.ADD_RECT:
            add_rounded_rect(tree, color)
        elif action == EditActions.MAKE_WHITE:
            make_colored(tree, color, "#ffffff")

    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(str(output), xml_declaration=True, method='xml', encoding='UTF-8', standalone=False)


RX_COLOR: re.Pattern = re.compile(r"stroke:(#[a-fA-F\d]{6})")


def get_color(tree: etree.ElementTree) -> str:
    """
    Get the color of the outer circle.
    """
    for child in tree.findall("{http://www.w3.org/2000/svg}ellipse"):
        if 'id' in child.attrib and 'style' in child.attrib and child.attrib['id'] and child.attrib['id'] == "circle":
            match = RX_COLOR.search(child.attrib['style'])
            if match is not None:
                return match.group(1)


def remove_circle(tree: etree.ElementTree):
    """
    Remove the circle.
    """
    root = tree.getroot()
    for child in tree.findall("{http://www.w3.org/2000/svg}ellipse"):
        if 'id' in child.attrib and child.attrib['id'] == "circle":
            root.remove(child)
            break


def add_rounded_rect(tree: etree.ElementTree, color: str):
    """
    Add a rounded rectangle.
    """
    root = tree.getroot()
    rect = etree.Element('rect')
    rect.attrib['id'] = "rect"
    rect.attrib['style'] = f"fill:none;stroke:{color};stroke-width:60;stroke-opacity:1;paint-order:fill markers stroke;stop-color:#000000"
    rect.attrib['width'] = "964"
    rect.attrib['height'] = "964"
    rect.attrib['x'] = "30"
    rect.attrib['y'] = "30"
    rect.attrib['rx'] = "192"
    rect.attrib['ry'] = "192"

    root.append(rect)


def make_colored(tree: etree.ElementTree, origin_color: str, new_color: str):
    """
    Makes the svg white.
    """
    for child in tree.iter():
        if 'style' in child.attrib:
            child.attrib['style'] = child.attrib['style'].replace(origin_color, new_color)
