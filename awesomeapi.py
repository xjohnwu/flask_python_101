from flask import Flask
from flask_restful import Resource, Api
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_apispec.extension import FlaskApiSpec
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin


class AwesomeResponseSchema(Schema):
    message = fields.Str(default='Success')


class AwesomeRequestSchema(Schema):
    api_type = fields.String(required=True, description="API type of awesome API")
    optional = fields.String(description='Optional type of awesome API')


#  Restful way of creating APIs through Flask Restful
class AwesomeAPI(MethodResource, Resource):
    @doc(description='My First GET Awesome API.', tags=['Awesome'])
    @marshal_with(AwesomeResponseSchema)  # marshalling
    def get(self):
        '''
        Get method represents a GET API method
        '''
        return {'message': 'My First Awesome API'}

    @doc(description='My First POST Awesome API.', tags=['Awesome'])
    @use_kwargs(AwesomeRequestSchema, location='json')
    @marshal_with(AwesomeResponseSchema)  # marshalling
    def post(self, **kwargs):
        '''
        Post method represents a POST API method
        '''
        return {'message': f"My Awesome API type: {kwargs['api_type']}"}


# 1. Initiate Flask app instance
app = Flask(__name__)
# 2. Flask restful wraps Flask app around it.
api = Api(app)
# 3. Flask-apispec extension to generate swagger API documentation
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    # 'APISPEC_SWAGGER_URL': '/swagger/',  # default URI to access API Doc JSON
    # 'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # default URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

# 4. Use Flask restful way to add a view resource. Internally it will call app/blueprint.add_url_rule()
api.add_resource(AwesomeAPI, '/awesome')
# 5. Register the same view with swagger doc
docs.register(AwesomeAPI)

if __name__ == '__main__':
    app.run(debug=True)
