from flask import Flask, render_template

import configuration
import controller
import dto
import persistence.model
import persistence.repository
import service
import util
from configuration.logging_configuration import logging as log
from controller import blueprints
from persistence.repository import ca_repository_bean

[log.info(f"Init {_module}") for _module in [configuration,
                                             controller,
                                             dto,
                                             persistence,
                                             persistence.model,
                                             persistence.repository,
                                             service,
                                             util]]

app = Flask(__name__)

for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.route("/view/<ca_id>")
def view(ca_id):
    # fetch details from DB using ca_id
    return render_template("view.html", ca_id=ca_id, domain=ca_repository_bean.find_ca_by_id(ca_id).domain)


if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=5000,
            debug=False)
