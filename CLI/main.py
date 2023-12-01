import argparse
import fnmatch
import logging
import os
import sys
import textwrap


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
        
    )
    
    parser = argparse.ArgumentParser(
        description="Static Analyzer - Prototype Project",
        formatter_class = argparse.RawDescriptionHelpFormatter,
    ) 
    parser.add_argument(
        "-r",
        "--recursive",
        dest="recursive",
        action="store_true",
        help="find and process files in subdirectories",
    )
    par