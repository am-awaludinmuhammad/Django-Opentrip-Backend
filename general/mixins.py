from general import constants

class CustomSerializerErrorMessagesMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.error_messages['required'] = constants.ERROR_REQUIRED_FIELD
            field.error_messages['blank'] = constants.ERROR_REQUIRED_FIELD
            field.error_messages['null'] = constants.ERROR_REQUIRED_FIELD