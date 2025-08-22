from typing import List

from flask import Blueprint, render_template, redirect, url_for, request

import util.view_util as view_util
from configuration.logging_configuration import logger as log
from persistence.model.ca_entity import CAEntity
from service import ca_service_bean, certificate_service_bean

view_controller_bp = Blueprint('view_controller', __name__, )


@view_controller_bp.route("/")
def view_certification_authorities():
    from persistence.repository import ca_repository_bean
    domains: List[CAEntity] = ca_repository_bean.find_all()
    return render_template('index.html', domains=domains)


@view_controller_bp.route('/certification-authority/<ca_id>')
def view_certification_authority(ca_id):
    from persistence.repository import certificate_repository_bean
    from persistence.repository import ca_repository_bean
    certification_authority = ca_repository_bean.find_ca_by_id(ca_id)
    certificates = certificate_repository_bean.find_certificates_by_ca(ca_id=ca_id)
    return render_template('view.html', certification_authority=certification_authority, certificates=certificates)


@view_controller_bp.route('/view/ca', methods=['POST'])
def create_ca():
    service_request = view_util.extract_ca_create_request(request=request)
    ca_service_bean.create_ca(ca_data=service_request)
    return redirect(url_for("view_controller.view_certification_authorities"))


@view_controller_bp.route('/view/certificate', methods=['POST'])
def create_certificate():
    log.info(request.form)
    service_request = view_util.extract_certificate_create_request(request=request)
    certificate_service_bean.create_certificate(certificate_data=service_request)
    return redirect(url_for("view_controller.view_certification_authority", ca_id=service_request.ca_id))
