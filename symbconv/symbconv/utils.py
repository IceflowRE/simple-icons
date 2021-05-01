from pathlib import Path


def get_paths(source: Path, output: Path, recursive: bool) -> list[tuple[Path, Path]]:
    """
    Generate output file paths based on input and combine them.
    """
    if output.is_file():
        raise ValueError("output cannot be a file.")
    if source.is_file():
        return [(source, output.joinpath(source.name))]

    # both directories
    if recursive:
        files = source.glob('**/*.svg')
    else:
        files = source.glob('*.svg')
    files = list(files)
    output_files = [output.joinpath(file.relative_to(source)) for file in files]
    return [(files[idx], output_files[idx]) for idx in range(0, len(files))]
