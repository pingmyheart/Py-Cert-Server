from flask import Blueprint, jsonify

from configuration import mongodb_bean
from configuration.logging_configuration import logger as log
from util.mongo_util import is_mongo_connected

actuator_bp = Blueprint('actuator', __name__, url_prefix='/actuator')


@actuator_bp.route('/health', methods=['GET'])
def health():
    log.info("[INCOMING REQUEST] - Health actuator")
    response = __response()
    return jsonify(response), 200 if response["status"] == "UP" else 503


@actuator_bp.route('/readiness', methods=['GET'])
def readiness():
    log.info("[INCOMING REQUEST] - Ready actuator")
    response = __response()
    return jsonify(response), 200 if response["status"] == "UP" else 503


def __response():
    mongo_status = is_mongo_connected(mongo_client=mongodb_bean)
    return {
        "status": "DOWN" if any([mongo_status]) is False else "UP",
        "components": {
            "mongodb": {
                "status": "UP" if mongo_status else "DOWN"
            }
        }
    }
