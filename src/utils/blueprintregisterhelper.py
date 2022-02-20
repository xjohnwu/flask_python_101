from flask import Blueprint
from flask_restful import Api
from flask_apispec.extension import FlaskApiSpec


class BlueprintRegisterHelper:
    def __init__(self, name, url_prefix):
        self.blueprint = Blueprint(name=name, import_name=name, url_prefix=url_prefix)
        self.blueprint_api = Api(self.blueprint)
        self.type_initiators = []

    def add_resource(self, subpath: str, type_: type, **resource_class_kwargs):
        self.blueprint_api.add_resource(type_, subpath, resource_class_kwargs=resource_class_kwargs)
        self.type_initiators.append((type_, resource_class_kwargs))

    def register_doc(self, docs: FlaskApiSpec):
        docs.app.register_blueprint(self.blueprint)
        for type_, resource_class_kwargs in self.type_initiators:
            docs.register(type_, blueprint=self.blueprint.name, resource_class_kwargs=resource_class_kwargs)