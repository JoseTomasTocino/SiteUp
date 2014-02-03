from django.core.exceptions import ValidationError


class ValidateAnyOf(object):
    """Receives a list of validators for a model field, and checks
    if ANY of those validators passes. Raises ValidationError otherwise."""

    def __init__(self, *validators):
        self.validators = validators

    def __call__(self, value):
        errors = []
        for validator in self.validators:
            try:
                validator(value)
                return
            except ValidationError as e:
                errors.append(unicode(e.message) % e.params)

        raise ValidationError('Combined validation failed: ' + ' '.join(errors))