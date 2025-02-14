from assertpy import assert_that
from cerberus import Validator

def validate_schema(object_to_validate, validation_schema, logger):
    validator = Validator(validation_schema, require_all=True)
    is_valid = validator.validate(object_to_validate)

    if not is_valid:
        logger("Validation failed for object:", object_to_validate)
        logger("Validation schema:", validation_schema)
        logger("Validation errors:", validator.errors)

    assert_that(is_valid, description=validator.errors).is_true()