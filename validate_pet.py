from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

import uuid


from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace

app = Flask(__name__)
api = Api(app, version='1.1', title='Validation API',
          description='A simple Validation API')

# Enums
PET_STATUS = ['available', 'sold', 'pending']
PET_TYPE = ['cat', 'dog', 'fish']

# Models
pet_model = api.model('Pet', {
    'id': fields.Integer(description='The pet ID'),
    'name': fields.String(required=True, description='The pet name'),
    'type': fields.String(required=True, description='The pet type', enum=PET_TYPE),
    'status': fields.String(description='The pet status', enum=PET_STATUS)
})

# Namespaces
validation_ns = Namespace('Validation', description='Validation operations')

api.add_namespace(validation_ns)

@validation_ns.route('/validate_pet')
class PetValidationResource(Resource):
    @validation_ns.doc('validate_pet')
    @validation_ns.expect(pet_model)
    def post(self):
        """Validate a pet against the pet model"""
        payload = api.payload
        # Validate the payload against the schema defined in schemas.py
        try:
            validate(instance=payload, schema=schemas.pet)
            # Additional validation logic can be added here if needed
            return {"message": "Validation successful"}, 200
        except Exception as e:
            return {"message": f"Validation failed: {str(e)}"}, 400
        
        
@validation_ns.route('/validate_pet_status/<string:status>')        
class PetValidationStatusResource(Resource):
    @validation_ns.doc('validate_pet_status')
    def post(self, status: str):
        """Validate pet status"""
        valid_statuses = ['available', 'sold', 'pending', 'reserved']
        # Validate the status
        try:
            if status not in valid_statuses:
                return {"message": f"Invalid status: {status}"}, 400
            return {"message": f"Status '{status}' is valid"}, 200
        except Exception as e:
            return {"message": f"Validation failed: {str(e)}"}, 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
