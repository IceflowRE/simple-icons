import shutil
from pathlib import Path

from symbconv.edit import EditActions as EA
"""
Licensed under the MIT license.
"""

from symbconv.edit import edit_svg_batch
from symbconv.export import optimize_svg, minimize_svg, export_batch
from symbconv.utils import get_paths

if __name__ == '__main__':
    source = Path("./icons/static/")
    gen_path = Path("./gen/")
    raw_path = gen_path / "raw"

    shutil.copytree(Path("./icons/static/"), raw_path / "circle-colored", dirs_exist_ok=True)
    edit_svg_batch(get_paths(source, raw_path / "circle-white/", True), [EA.MAKE_WHITE], "Generate Circle White")
    edit_svg_batch(get_paths(source, raw_path / "pure-colored/", True), [EA.REMOVE_CIRCLE], "Generate Pure Colored")
    edit_svg_batch(get_paths(source, raw_path / "pure-white/", True), [EA.REMOVE_CIRCLE, EA.MAKE_WHITE], "Generate Pure White")
    edit_svg_batch(get_paths(source, raw_path / "rectangle-colored/", True), [EA.REMOVE_CIRCLE, EA.ADD_RECT], "Generate Rectangle Colored")
    edit_svg_batch(get_paths(source, raw_path / "rectangle-white/", True), [EA.REMOVE_CIRCLE, EA.ADD_RECT, EA.MAKE_WHITE], "Generate Rectangle White")

    opt_path = gen_path / "optimized"
    min_path = gen_path / "minimized"
    for path in raw_path.glob('**'):
        (opt_path / path.relative_to(raw_path)).mkdir(parents=True, exist_ok=True)
        (min_path / path.relative_to(raw_path)).mkdir(parents=True, exist_ok=True)
    export_batch(get_paths(raw_path, opt_path, True), optimize_svg, "Optimize svg")
    export_batch(get_paths(raw_path, min_path, True), minimize_svg, "Minimize svg")
