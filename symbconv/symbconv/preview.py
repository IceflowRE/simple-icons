import io
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PreviewItem:
    path: Path
    name: str
    target: str = ""


def _gen_table(columns: int, max_idx: int) -> str:
    """
    Create a rst table.
    """
    table = io.StringIO()

    seperator = "========  " * columns + "\n"
    images = ""
    desc = ""
    table.write(seperator)
    for idx in range(max_idx):
        if idx != 0 and idx % columns == 0:
            table.write(images + "\n")
            table.write(desc + "\n")
            images = ""
            desc = ""
        elif idx != 0:
            images += "  "
            desc += "  "
        images += f"|svg{str(idx).zfill(3)}|"
        desc += f"|dsc{str(idx).zfill(3)}|"
    if images != "":
        table.write(images + "\n")
        table.write(desc + "\n")
    table.write(seperator)

    return table.getvalue()


def generate_overview_table(items: list[PreviewItem], columns: int) -> str:
    """
    Generate icon overview table.
    """
    preview = io.StringIO()
    preview.write(_gen_table(columns, len(items)))
    preview.write("\n\n")

    idx = -1
    for item in items:
        idx += 1
        preview.write(f".. |dsc{str(idx).zfill(3)}| replace:: {item.name}\n")
        image_path = str(item.path).replace('\\', '/')
        if item.target == "":
            target = str(item.path).replace('\\', '/')
        else:
            target = item.target
        preview.write(
            f".. |svg{str(idx).zfill(3)}| image:: {image_path}\n"
            "    :width: 128px\n"
            f"    :target: {target}\n"
        )

    return preview.getvalue()


def download_link(category: str) -> str:
    return f"https://github.com/IceflowRE/simple-icons/releases/download/latest/{category}.zip"


def template(caption: str, category: str, table: str):
    """
    Preview template for the icons.
    """
    io_str = io.StringIO()
    io_str.write(f"""{caption}
{'=' * len(caption)}

`Back to home <README.rst>`__

Downloads
---------

- `optimized svg <{download_link(category + '-optimized')}>`__ (recommended)
- `minimized svg <{download_link(category + '-minimized')}>`__ (for low bandwidth hosts)

Preview
-------

Click on the images to display it.

{table}
""")

    return io_str.getvalue()


def generate_main(table: str) -> str:
    """
    Main entry point to the icon preview.
    """
    io_str = io.StringIO()
    io_str.write(f"""Preview
=======

Read more about Iceflower's simple icons on the `main page <https://github.com/IceflowRE/simple-icons#readme>`__.

The following categories exist as an optimized svg and as an minimized svg.\n\n
Click on the images to get a preview of all icons.

{table}
""")
    return io_str.getvalue()
