import logging
import sys

from CLI.parse import parse_args


BASE_CONFIG = "staticanalyze.yaml"
LOG = logging.getLogger()

def _init_logger(log_level=logging.INFO, log_format=None):
    
    """ Logger Initializing
        :debug:
        :return:
    
    """
    
    LOG.handlers = []
    
    if not log_format:
        log_format_string = constants.log_format_string
    else:
        log_format_string = log_format
    
    logging.captureWarnings(True)
    
    LOG.setLevel(log_level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(log_format_string))
    LOG.addHandler(handler)
    LOG.debug("logging initialized")

def _log_option_source(default_val, arg_val, ini_val, option_name):
    """ to show the source of each option. """
    
    if default_val is None:
        if arg_val:
            LOG.info("Using command ling arg for %s", option_name)
            return arg_val
        elif ini_val:
            LOG.info("Using ini file for %s", option_name)
            return ini_val
        else:
            return None
    elif default_val == arg_val:
        return ini_val if ini_val else arg_val
    else: 
        return arg_val
    
def _log_info(args, profile):
    inc = ",".joing([t for t in profile["include"]]) or "None"
    exc = ",".join([t for t in profile["exclude"]]) or "None"
    LOG.info("profile include tests: %s", inc)
    LOG.info("profile exclude tests: %s", exc)
    LOG.info("cli include tests: %s", args.tests)
    LOG.info("cli exclude tests: %s", args.skips)
    
    
def main():
    """ STATIC ANALYZER CLI. """
    debug = (
        logging.DEBUG
        if "-d" in sys.argv or "--debug" in sys.argv
        else logging.INFO
    )
    _init_logger(debug)
    
    baseline_formatters = [
        f.name
        for f in filter(
            lambda x: hasattr(x.plugin,"_accepts_baseline"),
            
        )
    ]
    parser = parse_args().parser
    
    parser.set_defaults(debug=False)
    parser.set_defaults(verbose=False)
    parser.set_defaults(quiet=False)
    parser.set_defaults(ignore_nosec=False)

    #setup - parsing arguments
    args = parser.parse_args()
    
    if args.severity_string is not None:
        if args.severity_string == "all":
            args.severity = 1
        elif args.severity_string == "low":
            args.severity = 2
        elif args.severity_string == "medium":
            args.severity = 3
        elif args.severity_string == "high":
            args.severity = 4
    
    
if __name__ == "__main__":
    main()