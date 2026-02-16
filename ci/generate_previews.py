import shutil
from pathlib import Path

"""
Licensed under the MIT license.
"""
from symbconv import preview

if __name__ == '__main__':
    shutil.copytree(Path("./gen/minimized/"), Path("./preview/icons/"), dirs_exist_ok=True)

    # icon path for the preview
    icon_path = Path("./icons")
    previews = []
    category_preview = preview.generate_overview_table([
        preview.PreviewItem(icon_path / "circle-colored/particles.svg", "Circle Colored", "./preview-circle-colored.rst"),
        preview.PreviewItem(icon_path / "circle-white/particles.svg", "Circle White", "./preview-circle-white.rst"),
        preview.PreviewItem(icon_path / "rectangle-colored/particles.svg", "Rectangle Colored", "./preview-rectangle-colored.rst"),
        preview.PreviewItem(icon_path / "rectangle-white/particles.svg", "Rectangle White", "./preview-rectangle-white.rst"),
        preview.PreviewItem(icon_path / "pure-colored/particles.svg", "Pure Colored", "./preview-pure-colored.rst"),
        preview.PreviewItem(icon_path / "pure-white/particles.svg", "Pure White", "./preview-pure-white.rst"),
    ], 4)
    previews.append(("README.rst", preview.generate_main(category_preview)))

    # switch to the current icon path for iteration
    preview_path = Path("./preview/")
    icon_path = Path("./preview/icons")
    for path in icon_path.rglob("*"):
        if not path.is_dir():
            continue

        items = [preview.PreviewItem(file.relative_to(preview_path), str(file.relative_to(path))[:-4].replace("_", " ").replace("-", " ").title()) for file in
                 path.glob('**/*.svg')]
        items.sort(key=lambda val: val.name)
        table = preview.generate_overview_table(items, 5)
        category = str(path.relative_to(icon_path))
        caption = category.replace("-", " ").capitalize()
        text = preview.template(caption, category, table)
        previews.append((f"preview-{category}.rst", text))

    for name, text in previews:
        with (Path("./preview/") / name).open('w') as writer:
            writer.write(text)
