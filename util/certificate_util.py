from datetime import datetime, timezone

from cryptography import x509
from cryptography.hazmat.backends import default_backend

from configuration.logging_configuration import logger as log


def is_certificate_valid(cert_data: str) -> bool:
    cert = x509.load_pem_x509_certificate(str.encode(cert_data), default_backend())

    # Extract validity
    not_before = cert.not_valid_before
    not_after = cert.not_valid_after
    now = datetime.now(timezone.utc)

    print(f"Valid from: {not_before}")
    print(f"Valid until: {not_after}")

    if now < not_before:
        log.error("❌ Certificate is not valid yet.")
        return False
    elif now > not_after:
        log.error("❌ Certificate has expired.")
        return False
    else:
        log.info("✅ Certificate is valid.")
        return True
