from flask import Blueprint
from flask_restful import Resource, Api
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from flask_apispec.extension import FlaskApiSpec
from marshmallow import Schema, fields

from src.utils.blueprintregisterhelper import BlueprintRegisterHelper
from src.utils.dataservice import DataService


class TradingUniverseResponseSchema(Schema):
    trading_universe = fields.List(fields.String)


class TradingUniverseRequestSchema(Schema):
    first_n = fields.Integer(required=True, description="First N")


class TradingUniverseAPI(MethodResource, Resource):
    def __init__(self, data_service: DataService):
        self.data_service = data_service

    @doc(description='Symbols.', tags=['Data'])
    @use_kwargs(TradingUniverseRequestSchema, location='query')
    @marshal_with(TradingUniverseResponseSchema)  # marshalling
    def get(self, **kwargs):
        return {"trading_universe": self.data_service.get_symbols()[:kwargs['first_n']]}

    @doc(description='Filter first N symbols.', tags=['Data'])
    @use_kwargs(TradingUniverseRequestSchema, location='json')
    @marshal_with(TradingUniverseResponseSchema)  # marshalling
    def post(self, **kwargs):
        return {"trading_universe": self.data_service.get_symbols()[:kwargs['first_n']]}


def register_doc_old(docs: FlaskApiSpec):
    # 1. Create Blueprint
    blueprint_data = Blueprint(name='data', import_name='data', url_prefix='/api/v1/data')
    # 2. Wrap it with Api
    blueprint_data_api = Api(blueprint_data)

    # 3. Add resource
    data_service = DataService(['BTCUSDT', 'ETHUSDT', 'LTCUSDT', 'DYDXUSDT'])
    blueprint_data_api.add_resource(TradingUniverseAPI, '/universe',
                                    resource_class_kwargs={'data_service': data_service})
    # 4. Only register blueprint in app after adding all resources
    docs.app.register_blueprint(blueprint_data)

    # 5. Register swagger in the final step
    docs.register(TradingUniverseAPI, blueprint=blueprint_data.name,
                  resource_class_kwargs={'data_service': data_service})


def register_doc(docs: FlaskApiSpec):
    helper = BlueprintRegisterHelper(name='data', url_prefix='/api/v1/data')
    data_service = DataService(['BTCUSDT', 'ETHUSDT', 'LTCUSDT', 'DYDXUSDT'])
    helper.add_resource('/universe', TradingUniverseAPI, data_service=data_service)
    # helper.add_resource('/kline', KlineAPI)

    # Register swagger in the final step
    helper.register_doc(docs)
