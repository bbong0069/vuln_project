import argparse 
import os 
import sys

class ParsersArgs():
    parser = argparse.ArgumentParser(
        description="Bandit - a Python source code security analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "targets",
        metavar="targets",
        type=str,
        nargs="*",
        help="source file(s) or directory(s) to be tested",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        dest="recursive",
        action="store_true",
        help="find and process files in subdirectories",
    )
    parser.add_argument(
        "-a",
        "--aggregate",
        dest="agg_type",
        action="store",
        default="file",
        type=str,
        choices=["file", "vuln"],
        help="aggregate output by vulnerability (default) or by filename",
    )
    parser.add_argument(
        "-n",
        "--number",
        dest="context_lines",
        action="store",
        default=3,
        type=int,
        help="maximum number of code lines to output for each issue",
    )
    parser.add_argument(
        "-c",
        "--configfile",
        dest="config_file",
        action="store",
        default=None,
        type=str,
        help="optional config file to use for selecting plugins and "
        "overriding defaults",
    )
    parser.add_argument(
        "-p",
        "--profile",
        dest="profile",
        action="store",
        default=None,
        type=str,
        help="profile to use (defaults to executing all tests)",
    )
    parser.add_argument(
        "-t",
        "--tests",
        dest="tests",
        action="store",
        default=None,
        type=str,
        help="comma-separated list of test IDs to run",
    )
    parser.add_argument(
        "-s",
        "--skip",
        dest="skips",
        action="store",
        default=None,
        type=str,
        help="comma-separated list of test IDs to skip",
    )
    severity_group = parser.add_mutually_exclusive_group(required=False)
    severity_group.add_argument(
        "-l",
        "--level",
        dest="severity",
        action="count",
        default=1,
        help="report only issues of a given severity level or "
        "higher (-l for LOW, -ll for MEDIUM, -lll for HIGH)",
    )
    severity_group.add_argument(
        "--severity-level",
        dest="severity_string",
        action="store",
        help="report only issues of a given severity level or higher."
        ' "all" and "low" are likely to produce the same results, but it'
        " is possible for rules to be undefined which will"
        ' not be listed in "low".',
        choices=["all", "low", "medium", "high"],
    )
    confidence_group = parser.add_mutually_exclusive_group(required=False)
    confidence_group.add_argument(
        "-i",
        "--confidence",
        dest="confidence",
        action="count",
        default=1,
        help="report only issues of a given confidence level or "
        "higher (-i for LOW, -ii for MEDIUM, -iii for HIGH)",
    )
    confidence_group.add_argument(
        "--confidence-level",
        dest="confidence_string",
        action="store",
        help="report only issues of a given confidence level or higher."
        ' "all" and "low" are likely to produce the same results, but it'
        " is possible for rules to be undefined which will"
        ' not be listed in "low".',
        choices=["all", "low", "medium", "high"],
    )
    output_format = (
        "screen"
        if (
            sys.stdout.isatty()
            and os.getenv("NO_COLOR") is None
            and os.getenv("TERM") != "dumb"
        )
        else "txt"
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="output_format",
        action="store",
        default=output_format,
        help="specify output format",
        choices=sorted(extension_mgr.formatter_names),
    )
    parser.add_argument(
        "--msg-template",
        action="store",
        default=None,
        help="specify output message template"
        " (only usable with --format custom),"
        " see CUSTOM FORMAT section"
        " for list of available values",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        action="store",
        nargs="?",
        type=argparse.FileType("w", encoding="utf-8"),
        default=sys.stdout,
        help="write report to filename",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="output extra information like excluded and included files",
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="turn on debug mode",
    )
    group.add_argument(
        "-q",
        "--quiet",
        "--silent",
        dest="quiet",
        action="store_true",
        help="only show output in the case of an error",
    )
    parser.add_argument(
        "--ignore-nosec",
        dest="ignore_nosec",
        action="store_true",
        help="do not skip lines with # nosec comments",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        dest="excluded_paths",
        action="store",
        default=",".join(constants.EXCLUDE),
        help="comma-separated list of paths (glob patterns "
        "supported) to exclude from scan "
        "(note that these are in addition to the excluded "
        "paths provided in the config file) (default: "
        + ",".join(constants.EXCLUDE)
        + ")",
    )
    parser.add_argument(
        "-b",
        "--baseline",
        dest="baseline",
        action="store",
        default=None,
        help="path of a baseline report to compare against "
        "(only JSON-formatted files are accepted)",
    )
    parser.add_argument(
        "--ini",
        dest="ini_path",
        action="store",
        default=None,
        help="path to a .bandit file that supplies command line arguments",
    )
    parser.add_argument(
        "--exit-zero",
        action="store_true",
        dest="exit_zero",
        default=False,
        help="exit with 0, " "even with results found",
    )
    python_ver = sys.version.replace("\n", "")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {bandit.__version__}\n"
        f"  python version = {python_ver}",
    )


def _add_optional_group(parser):
    optional_group = parser.add_argument_group('optional arguments')
    optional_group.add_argument(
        
    )
    
def _add_required_group(parser):
    required_group = parser.add_argument_group('required arguments')
    required_group.add_argument(
        'targets', metavar='targets', nargs='+',
        help='source file(s) or directory to be scanned',
        
    )    

def parse_args(args):
    if len(args) == 0:
        args.append('-h')
    parser = argparse.ArgumentParser(prog='python -m staticanalyze')
    
    parser._action_groups.pop()
    
    _add_required_group(parser)
    