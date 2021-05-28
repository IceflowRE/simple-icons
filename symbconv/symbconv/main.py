import sys
from argparse import ArgumentParser
from pathlib import Path

from symbconv.edit import EditActions as EA
from symbconv.edit import edit_svg_batch
from symbconv.export import export_batch, optimize_svg, minimize_svg
from symbconv.utils import get_paths


def cmd_parser():
    parser = ArgumentParser(prog="symbconv", description="")

    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_edit_svg = subparsers.add_parser('edit', help='edit given svg')
    parser_edit_svg.add_argument('--clean_up', dest='clean_up', action='store_true', help='clean up selected not required inkcsape entries')
    parser_edit_svg.add_argument('--remove_circle', dest='remove_circle', action='store_true', help='remove circle from svg')
    parser_edit_svg.add_argument('--add_rect', dest='add_rect', action='store_true', help='add a rounded rectangle to the svg')
    parser_edit_svg.add_argument('--make_colored', dest='make_colored', action='store_true', help='make svg white')
    parser_edit_svg.add_argument('--recursive', dest='recursive', action='store_true',
                                 help="go through dir recursive, will be ignored if source is not a dir")
    parser_edit_svg.add_argument(dest='source', type=str, help='path to the input file or dir')
    parser_edit_svg.add_argument(dest='output', type=str, help='path to the output dir')

    parser_inkscape = subparsers.add_parser('export', help='export svg')
    parser_inkscape.add_argument('--recursive', dest='recursive', action='store_true', help="go through dir recursive, will be ignored if source is not a dir")
    parser_inkscape.add_argument(dest='export_mode', choices=['optimize', 'minimize'])
    parser_inkscape.add_argument(dest='source', type=str, help='path to the input file or dir')
    parser_inkscape.add_argument(dest='output', type=str, help='path to the output dir')

    return parser


def main():
    args = cmd_parser().parse_args(sys.argv[1:])

    success = False

    output = Path(args.output)
    if not output.exists():
        output.mkdir(parents=True, exist_ok=True)

    if args.command == 'edit':
        actions = []
        if args.clean_up:
            actions.append(EA.CLEAN_UP)
        if args.remove_circle:
            actions.append(EA.REMOVE_CIRCLE)
        if args.add_rect:
            actions.append(EA.ADD_RECT)
        if args.make_white:
            actions.append(EA.MAKE_WHITE)
        if len(actions) == 0:
            args.error('Provide at least one action.')

        success = edit_svg_batch(get_paths(Path(args.source).absolute(), output.absolute(), args.recursive), "Edit svg")

    if args.command == 'export':
        if args.export_mode == 'optimize':
            func = optimize_svg
            desc = "Optimize svg"
        elif args.export_mode == 'minimize':
            func = minimize_svg
            desc = "Minimize svg"
        export_batch(get_paths(Path(args.source).absolute(), output.absolute(), args.recursive), func, desc)
        success = True

    if success:
        exit(0)
    else:
        exit(1)
