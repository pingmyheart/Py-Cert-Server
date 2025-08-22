from persistence.repository import ca_repository_bean, certificate_repository_bean
from service.ca_service import CAService
from service.certificate_service import CertificateService

ca_service_bean = CAService(ca_repository=ca_repository_bean)
certificate_service_bean = CertificateService(certificate_repository=certificate_repository_bean,
                                              certificate_authority_service=ca_service_bean)
