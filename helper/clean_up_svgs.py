from pathlib import Path

from symbconv.edit import EditActions as EA
from symbconv.edit import edit_svg_batch
from symbconv.utils import get_paths

if __name__ == '__main__':
    source = Path("./icons/")
    edit_svg_batch(get_paths(source, source, True), [EA.CLEAN_UP], "Clean Up")
