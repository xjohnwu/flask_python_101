from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec

from src.endpoints import data

app = Flask("Flask REST API demo")  # Flask app instance initiated
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Flask REST API demo',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/api/v1/swagger.json',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/api/v1/swagger-ui/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)
data.register_doc(docs)
