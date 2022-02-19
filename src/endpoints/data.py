from flask import Blueprint
from flask_restful import Resource, Api
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from flask_apispec.extension import FlaskApiSpec
from marshmallow import Schema, fields

from src.utils.dataservice import DataService


class TradingUniverseResponseSchema(Schema):
    trading_universe = fields.List(fields.String)


class TradingUniverseAPI(MethodResource, Resource):
    def __init__(self, data_service: DataService):
        self.data_service = data_service

    @doc(description='Symbols.', tags=['Binance'])
    @marshal_with(TradingUniverseResponseSchema)  # marshalling
    def get(self):
        return {"trading_universe": self.data_service.get_symbols()}


def register_doc(docs: FlaskApiSpec):
    blueprint_data = Blueprint(name='data', import_name='data', url_prefix='/api/v1/data')

    blueprint_data_api = Api(blueprint_data)
    blueprint_data_api.add_resource(TradingUniverseAPI, '/universe',
                                    resource_class_kwargs={'data_service': DataService(['BTCUSDT', 'ETHUSDT'])})

    docs.app.register_blueprint(blueprint_data)

    docs.register(TradingUniverseAPI, blueprint=blueprint_data.name,
                  resource_class_kwargs={'data_service': DataService(['BTCUSDT', 'ETHUSDT'])})
