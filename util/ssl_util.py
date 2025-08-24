import base64
from datetime import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend

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


def parse_certificate(cert_b64: str):
    # Decode from base64
    cert_der = base64.b64decode(cert_b64)

    # Load certificate (DER format assumed)
    cert = x509.load_pem_x509_certificate(cert_der, default_backend())
    subject = cert.subject

    # Extract fields
    def get_attr(oid):
        try:
            return subject.get_attributes_for_oid(oid)[0].value
        except IndexError:
            return ""

    return {
        "domain": get_attr(x509.NameOID.COMMON_NAME),
        "country": get_attr(x509.NameOID.COUNTRY_NAME),
        "location": get_attr(x509.NameOID.LOCALITY_NAME),
        "state": get_attr(x509.NameOID.STATE_OR_PROVINCE_NAME),
        "organization": get_attr(x509.NameOID.ORGANIZATION_NAME),
        "organization_unit": get_attr(x509.NameOID.ORGANIZATIONAL_UNIT_NAME),
    }
