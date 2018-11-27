#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
import os
import re
import argparse
from collections import namedtuple
from fnmatch import fnmatch
from mastersign_config import Configuration
from mastersign_mysql import execute_sql_file


__version__ = '0.1.1'

SqlStep = namedtuple('SqlStep', ['no', 'name', 'script'])


def sql_steps(dir_path):
    result = []
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path) and fnmatch(file, '*.sql'):
            filename, __ = os.path.splitext(file)
            no, name = filename.split('_', 1)
            result.append(SqlStep(int(no), name, file_path))
    return sorted(result, key=lambda s: s.no)


def filter_steps(steps,
                 include_by_no=[], exclude_by_no=[],
                 from_no=None, to_no=None,
                 glob_include=None, glob_exclude=None,
                 re_include=None, re_exclude=None):
    if isinstance(re_include, str):
        re_include = re.compile(re_include)
    if isinstance(re_exclude, str):
        re_exclude = re.compile(re_exclude)
    return [
        step for step in steps
        if (not include_by_no or step.no in include_by_no) and \
           (not exclude_by_no or step.no not in exclude_by_no) and \
           (from_no is None or step.no >= from_no) and \
           (to_no is None or step.no <= to_no) and \
           (not glob_include or fnmatch(step.name, glob_include)) and \
           (not glob_exclude or not fnmatch(step.name, glob_exclude)) and \
           (not re_include or re_include.match(step.name)) and \
           (not re_exclude or not re_exclude.match(step.name))
    ]


def show_steps(steps):
    for no, name, script in steps:
        print('[{}] {}'.format(str(no).rjust(3, '0'), name))


def parse_args():
    parser = argparse.ArgumentParser(
        description='Run multiple SQL scripts on a MySQL server.')
    parser.add_argument('-v', '--version', action='version', version=__version__,
                        help='print the program version and exit')
    parser.add_argument('-d', '--dry', action='store_true',
                        help='do not run the scripts, just print the selected script names')
    parser.add_argument('-n', '--include-no', dest='include_by_no', nargs='*', type=int, metavar='NO',
                        help='include the listed steps by no')
    parser.add_argument('-xn', '--exclude-no', dest='exclude_by_no', nargs='*', type=int, metavar='NO',
                        help='exclude the listed steps by no')
    parser.add_argument('-f', '--from', dest='from_no', type=int, metavar='NO',
                        help='excludes steps with a number lower')
    parser.add_argument('-t', '--to', dest='to_no', type=int, metavar='NO',
                        help='exclude steps with a number higher')
    parser.add_argument('-g', '--include', dest='glob_include', type=str, metavar='PATTERN',
                        help='include steps, which name matches the given glob pattern')
    parser.add_argument('-xg', '--exclude', dest='glob_exclude', type=str, metavar='PATTERN',
                        help='exclude steps, which name matches the given glob pattern')
    parser.add_argument('-r', '--include-re', dest='re_include', type=str, metavar='REGEX',
                        help='include steps, which name matches the given regex')
    parser.add_argument('-xr', '--exclude-re', dest='re_exclude', type=str, metavar='REGEX',
                        help='include steps, which name matches the given regex')
    parser.add_argument('source_dir', metavar='SOURCE_DIR',
                        help='A path to the directory with SQL scripts named <no>_<name>.sql.')
    parser.add_argument('target', metavar='TARGET_SERVER',
                        help='The name of the target database in the configuration. '
                        'This is the database to execute the scripts on.')

    Configuration.add_config_arguments(parser)
    return parser.parse_args()


def run():
    args = parse_args()
    cfg = Configuration.load(args)

    steps = filter_steps(sql_steps(args.source_dir),
                         include_by_no=args.include_by_no,
                         exclude_by_no=args.exclude_by_no,
                         from_no=args.from_no,
                         to_no=args.to_no,
                         glob_include=args.glob_include,
                         glob_exclude=args.glob_exclude,
                         re_include=args.re_include,
                         re_exclude=args.re_exclude)

    if args.dry:
        show_steps(steps)
    else:
        for step in steps:
            print('Executing [{}] {} ...'.format(str(step.no).rjust(3, '0'), step.name))
            if not execute_sql_file(cfg, args.target, step.script):
                print('Executing [{}] {} FAILED'.format(str(step.no).rjust(3, '0'), step.name))
                return 1

        print('Finished.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(run())
    except KeyboardInterrupt:
        print('\nCancelled by user.')
        sys.exit(1)
