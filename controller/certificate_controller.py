import base64

from flask import request, Blueprint, jsonify, Response

from dto.ca_dto import GenerateCertificateAuthorityRequest
from dto.certificate_dto import GenerateCertificateRequest
from service import ca_service_bean, certificate_service_bean

certificate_controller_bp = Blueprint('certificate_controller', __name__, url_prefix='/certificate')


@certificate_controller_bp.route('/ca', methods=['POST'])
def generate_certificate_ca():
    request_data = GenerateCertificateAuthorityRequest(**request.get_json())
    service_response = ca_service_bean.create_ca(ca_data=request_data)
    return (jsonify(service_response.dict(exclude_none=True)),
            200)


@certificate_controller_bp.route('/ca/download/<ca_id>', methods=['GET'])
def download_certificate_ca(ca_id):
    service_response = ca_service_bean.get_ca_by_id(ca_id=ca_id)
    certificate = base64.b64decode(service_response.crt).decode("utf-8")
    return Response(
        certificate,
        mimetype='text/plain',
        headers={"Content-Disposition": f"attachment;filename={service_response.domain}.ca.crt"}
    )


@certificate_controller_bp.route('/download/<certificate_id>/crt', methods=['GET'])
def download_certificate(certificate_id):
    service_response = certificate_service_bean.get_certificate(certificate_id=certificate_id)
    certificate = base64.b64decode(service_response.crt).decode("utf-8")
    return Response(
        certificate,
        mimetype='text/plain',
        headers={"Content-Disposition": f"attachment;filename={service_response.domain}.crt"}
    )


@certificate_controller_bp.route('/download/<certificate_id>/key', methods=['GET'])
def download_certificate_key(certificate_id):
    service_response = certificate_service_bean.get_certificate(certificate_id=certificate_id)
    certificate = base64.b64decode(service_response.key).decode("utf-8")
    return Response(
        certificate,
        mimetype='text/plain',
        headers={"Content-Disposition": f"attachment;filename={service_response.domain}.key"}
    )


@certificate_controller_bp.route('', methods=['POST'])
def generate_certificate():
    service_request = GenerateCertificateRequest(**request.get_json())
    service_response = certificate_service_bean.create_certificate(certificate_data=service_request)
    return ("success",
            200)
