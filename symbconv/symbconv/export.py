import optparse
from pathlib import Path

from scour import scour
from tqdm import tqdm


def export_batch(paths: list[tuple[Path, Path]], func, desc: str):
    """
    Export based on a path list.
    """
    for source, output in tqdm(paths, total=len(paths), desc=desc, unit='svg', mininterval=1, ncols=100, disable=False):
        try:
            func(source, output)
        except Exception as ex:
            tqdm.write(f"Failed to apply changes to '{source}': {str(ex)}")


def minimize_svg(in_path: Path, out_path: Path):
    """
    Minimize file size of a svg.
    """
    options = optparse.Values({
        'infilename': str(in_path), 'outfilename': str(out_path),
        'digits': 5, 'quiet': True, 'verbose': False, 'cdigits': -1, 'simple_colors': True,
        'style_to_xml': True, 'group_collapse': True, 'group_create': False, 'keep_editor_data': False, 'keep_defs': False, 'renderer_workaround': True,
        'strip_xml_prolog': False, 'remove_titles': True, 'remove_descriptions': True, 'remove_metadata': True, 'remove_descriptive_elements': True,
        'strip_comments': True, 'embed_rasters': True, 'enable_viewboxing': True, 'indent_type': 'none', 'indent_depth': 0, 'newlines': False,
        'strip_xml_space_attribute': True, 'strip_ids': True, 'shorten_ids': True, 'shorten_ids_prefix': '', 'protect_ids_noninkscape': False,
        'protect_ids_list': None, 'protect_ids_prefix': None, 'error_on_flowtext': False
    })
    in_file, out_file = scour.getInOut(options)
    scour.start(options, in_file, out_file)


def optimize_svg(in_path: Path, out_path: Path):
    """
    Optimize svg file, but keep metadata.
    """
    options = optparse.Values({
        'infilename': str(in_path), 'outfilename': str(out_path),
        'digits': 5, 'quiet': True, 'verbose': False, 'cdigits': -1, 'simple_colors': True,
        'style_to_xml': True, 'group_collapse': True, 'group_create': False, 'keep_editor_data': False, 'keep_defs': False, 'renderer_workaround': True,
        'strip_xml_prolog': False, 'remove_titles': False, 'remove_descriptions': False, 'remove_metadata': False, 'remove_descriptive_elements': False,
        'strip_comments': True, 'embed_rasters': True, 'enable_viewboxing': True, 'indent_type': 'none', 'indent_depth': 0, 'newlines': False,
        'strip_xml_space_attribute': False, 'strip_ids': True, 'shorten_ids': True, 'shorten_ids_prefix': '', 'protect_ids_noninkscape': False,
        'protect_ids_list': None, 'protect_ids_prefix': None, 'error_on_flowtext': False
    })
    in_file, out_file = scour.getInOut(options)
    scour.start(options, in_file, out_file)
