import util.ssl_util as ssl_util
from service import CertificateService, CAService


class UpdateCertificateScheduler:
    def __init__(self, certificate_service: CertificateService, certification_authority_service: CAService):
        self.certificate_service = certificate_service
        self.certification_authority_service = certification_authority_service

    def schedule(self):
        for ca in self.certification_authority_service.find_all():
            if ssl_util.get_certificate_expires_in_days(ca.crt) <= 7:
                self.certification_authority_service.renew(ca_id=ca.ca_id)
                self.__renew_ca_certificates(ca_id=ca.ca_id)
            else:
                self.__renew_ca_certificates(ca_id=ca.ca_id)

    def __renew_ca_certificates(self, ca_id: str):
        for certificate in self.certificate_service.get_certificates_by_ca(ca_id=ca_id):
            self.certificate_service.renew(certificate_id=certificate.certificate_id)
