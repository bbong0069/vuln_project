import json
from datetime import datetime

def report(
    vulnerabilities,
    fileobj,
    print_sanitised,
):    
    TZ_AGNOSTIC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    time_string = datetime.utcnow().strftime(TZ_AGNOSTIC_FORMAT)

    machine_output = {
        'generated_at': time_string,
        'vulnerabilities': [
            vuln.as_dict() for vuln in vulnerabilities
            if print_sanitised or not isinstance(vuln, SanitisedVulnerability)
        ]
    }

    result = json.dumps(
        machine_output,
        indent=4
    )

    with fileobj:
        fileobj.write(result)