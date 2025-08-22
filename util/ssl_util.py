from datetime import datetime

import util.shell_util as shell_util


def get_certificate_expires_in_days(certificate_data: str) -> int:
    """
    Get the number of days until the certificate expires.
    :param certificate_data: Certificate file data.
    :return: Number of days until expiration.
    """
    command = f"echo -n '{certificate_data}' | base64 -d | openssl x509 -enddate -noout"
    _, result = shell_util.run_command(command)
    end_date_str = result.strip().split('=')[1]
    end_date = datetime.strptime(end_date_str, '%b %d %H:%M:%S %Y %Z')
    return (end_date - datetime.now()).days
