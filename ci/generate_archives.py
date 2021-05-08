"""
Licensed under the MIT license.
"""

import shutil
from pathlib import Path

if __name__ == '__main__':
    gen_path = Path("./gen")
    (gen_path / "archives").mkdir(parents=True, exist_ok=True)
    for typ in ["minimized", "optimized"]:
        icon_path = gen_path / typ
        for path in icon_path.glob("**"):
            if path == icon_path:
                continue
            output_file = gen_path / "archives" / f"{path.relative_to(icon_path)}-{typ}"
            print(f"zip {path}")
            shutil.make_archive(output_file, 'zip', path)
