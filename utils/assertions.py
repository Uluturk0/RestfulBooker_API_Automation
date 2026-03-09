import json
import os
from jsonschema import validate, ValidationError

def assert_valid_schema(data: dict, schema_file: str):
    """
    Validates a JSON dictionary against a predefined JSON Schema file.
    """
    current_dir = os.path.dirname(__file__)
    schema_path = os.path.join(current_dir, '..', 'schemas', schema_file)
    
    with open(schema_path, 'r') as file:
        schema = json.load(file)
        
    #  We compare the API's data with our schema
    try:
        validate(instance=data, schema=schema)
    except ValidationError as err:
        raise AssertionError(f"Schema Validation Failed! Error: {err.message}")