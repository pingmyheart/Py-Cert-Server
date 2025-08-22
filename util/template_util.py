from string import Template

from configuration.logging_configuration import logger as log


def generate_cert_conf(domain: str):
    log.info("Generating certificate configuration")
    raw_conf = """
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = $domain
"""
    template = Template(raw_conf)
    return template.substitute(domain=domain)


def generate_csr_conf(country: str,
                      state: str,
                      location: str,
                      organization: str,
                      organization_unit: str,
                      domain: str):
    log.info("Generating CSR configuration")
    raw_conf = """
    [ req ]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[ dn ]
C = $country
ST = $state
L = $location
O = $organization
OU = $organization_unit
CN = $domain

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = $domain
# DNS.2 = www.%SUB_DOMAIN_NAME%
# IP.1 = 127.0.0.1
# IP.2 = 127.0.0.1
"""
    template = Template(raw_conf)
    return template.substitute(country=country,
                               state=state,
                               location=location,
                               organization=organization,
                               organization_unit=organization_unit,
                               domain=domain)
