from flask import Blueprint
from flask_restful import Resource, Api
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from flask_apispec.extension import FlaskApiSpec
from marshmallow import Schema, fields

from src.utils.dataservice import DataService


class TradingUniverseResponseSchema(Schema):
    trading_universe = fields.List(fields.String)


class TradingUniverseRequestSchema(Schema):
    first_n = fields.Integer(required=True, description="First N")


class TradingUniverseAPI(MethodResource, Resource):
    def __init__(self, data_service: DataService):
        self.data_service = data_service

    @doc(description='Symbols.', tags=['Binance'])
    @use_kwargs(TradingUniverseRequestSchema, location='query')
    @marshal_with(TradingUniverseResponseSchema)  # marshalling
    def get(self, **kwargs):
        return {"trading_universe": self.data_service.get_symbols()[:kwargs['first_n']]}

    @doc(description='Filter first N symbols.', tags=['Binance'])
    @use_kwargs(TradingUniverseRequestSchema, location='json')
    @marshal_with(TradingUniverseResponseSchema)  # marshalling
    def post(self, **kwargs):
        return {"trading_universe": self.data_service.get_symbols()[:kwargs['first_n']]}


def register_doc(docs: FlaskApiSpec):
    blueprint_data = Blueprint(name='data', import_name='data', url_prefix='/api/v1/data')

    blueprint_data_api = Api(blueprint_data)

    data_service = DataService(['BTCUSDT', 'ETHUSDT', 'LTCUSDT', 'DYDXUSDT'])
    blueprint_data_api.add_resource(TradingUniverseAPI, '/universe',
                                    resource_class_kwargs={'data_service': data_service})

    docs.app.register_blueprint(blueprint_data)

    docs.register(TradingUniverseAPI, blueprint=blueprint_data.name,
                  resource_class_kwargs={'data_service': data_service})
