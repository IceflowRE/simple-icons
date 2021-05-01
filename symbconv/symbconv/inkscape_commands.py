import subprocess
from pathlib import Path


def export_plain(paths: list[tuple[Path, Path]]) -> bool:
    success = True

    for source, output in paths:
        process = subprocess.Popen(
            ['inkscape', "--export-plain-svg", f"--export-filename={output}", str(source)],
            stdout=subprocess.PIPE,
            universal_newlines=True
        )

        while True:
            output = process.stdout.readline()
            text = output.strip()
            if text != "":
                print(text)
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                success = False
                # Process has finished, read rest of the output
                for text in process.stdout.readlines():
                    text = text.strip()
                    if text != "":
                        print(text)
                break

        print(f"Converted: {source} -> {output} - {return_code}")
    return success
