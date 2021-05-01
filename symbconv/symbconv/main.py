import sys
from argparse import ArgumentParser
from pathlib import Path

from symbconv.edit_svg import edit_svg_entry
from symbconv.inkscape_commands import export_plain
from symbconv.edit_svg import EditActions as EA
from symbconv.utils import get_paths


def cmd_parser():
    parser = ArgumentParser(prog="symbconv", description="")

    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_edit_svg = subparsers.add_parser('edit', help='edit given svg')
    parser_edit_svg.add_argument('--remove_circle', dest='remove_circle', action='store_true', help='remove circle from svg')
    parser_edit_svg.add_argument('--add_rect', dest='add_rect', action='store_true', help='add a rounded rectangle to the svg')
    parser_edit_svg.add_argument('--make_colored', dest='make_colored', action='store_true', help='make svg white')
    parser_edit_svg.add_argument('--recursive', dest='recursive', action='store_true', help="go through folder recursive, will be ignored if source is not a folder")
    parser_edit_svg.add_argument(dest='source', type=str, help='path to the input file or folder')
    parser_edit_svg.add_argument(dest='output', type=str, help='path to the output folder')

    parser_inkscape = subparsers.add_parser('inkscape', help='inkscape commands')
    parser_inkscape.add_argument('--recursive', dest='recursive', action='store_true', help="go through folder recursive, will be ignored if source is not a folder")
    parser_inkscape.add_argument(dest='inkscape_cmd', choices=['export_plain', 'export_optimized'])
    parser_inkscape.add_argument(dest='source', type=str, help='path to the input file or folder')
    parser_inkscape.add_argument(dest='output', type=str, help='path to the output file or folder')

    return parser


def main():
    args = cmd_parser().parse_args(sys.argv[1:])

    success = True

    output = Path(args.output)
    if not output.exists():
        output.mkdir(parents=True, exist_ok=True)

    if args.command == 'edit':
        actions = []
        if args.remove_circle:
            actions.append(EA.REMOVE_CIRCLE)
        if args.add_rect:
            actions.append(EA.ADD_RECT)
        if args.make_white:
            actions.append(EA.MAKE_WHITE)
        if len(actions) == 0:
            args.error('Provide at least one action.')

        success = edit_svg_entry(get_paths(Path(args.source).absolute(), output.absolute(), args.recursive), actions)

    if args.command == 'inkscape':
        if args.inkscape_cmd == 'export_plain':
            success = export_plain(get_paths(Path(args.source).absolute(), output.absolute(), args.recursive))
        elif args.inkscape_cmd == 'export_optimized':
            pass

    if success:
        exit(0)
    else:
        exit(1)
