import argparse 
import os 
import sys



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
    