import json
from enum import Enum 
from collections import namedtuple

class VulnerabilityType(Enum):
    FALSE = 0 
    SANITISED = 1 
    TRUE = 2
    UNKOWN = 3
    
def vuln_factory(vulnerability_type):
    'ControlFlowNode',
    (
        'test',
        'last_nodes',
        'break_statements'
    )
