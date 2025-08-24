from flask import Flask

import configuration
import controller
import dto
import persistence.model
import persistence.repository
import scheduling
import service
import util
from configuration.logging_configuration import logging as log
from controller import blueprints

[log.info(f"Init {_module}") for _module in [configuration,
                                             controller,
                                             dto,
                                             persistence,
                                             persistence.model,
                                             persistence.repository,
                                             scheduling,
                                             service,
                                             util]]

app = Flask(__name__)

for blueprint in blueprints:
    app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=5000,
            debug=False)
