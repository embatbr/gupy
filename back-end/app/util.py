"""Useful and interchangeable code (e.g., error carrier)
"""


class DatabaseConstraintViolationError(Exception):

    def __init__(self, resource, field_name, field_value, constraint):
        self.resource = resource
        self.field_name = field_name
        self.field_value = field_value
        self.constraint = constraint

    class NOT_NULL(object):
        pass

    class UNIQUE(object):
        pass

    class PRIMARY_KEY(object):
        pass

    class PRIMARY_KEY(object):
        pass

    class CHECK(object):
        pass

    class EXCLUSION(object):
        pass


class DatabaseInvalidValueError(Exception):

    def __init__(self, resource, field_name):
        self.resource = resource
        self.field_name = field_name


class DomainError(Exception):

    def __init__(self, action, resource, reason):
        self.action = action
        self.resource = resource
        self.reason = reason

    def show(self):
        return {
            'action': self.action,
            'resource': self.resource,
            'reason': self.reason
        }


def handle_not_null_violation(error, resource):
    if str(error).startswith('null value in column'):
        raise DatabaseConstraintViolationError(resource, None, None,
            DatabaseConstraintViolationError.NOT_NULL)

def handle_enum_violation(enum_type, enum_field, error, resource):
    if str(error).startswith('invalid input value for enum %s' % enum_type):
        raise DatabaseInvalidValueError(resource, enum_field)

def handle_character_field_overflow(error, resource):
    if str(error).startswith('value too long for type character'):
        raise DatabaseInvalidValueError(resource, None)

def handle_numeric_field_overflow(error, resource):
    if str(error).startswith('numeric field overflow'):
        raise DatabaseInvalidValueError(resource, None)

def handle_unique_violation(error, resource, field_name, field_value):
    if str(error).startswith('duplicate key value violates unique constraint'):
        raise DatabaseConstraintViolationError(resource, field_name, field_value,
            DatabaseConstraintViolationError.UNIQUE)

def handle_date_or_time_out_of_range(error, resource, field_name):
    if str(error).startswith('date/time field value out of range'):
        raise DatabaseInvalidValueError(resource, field_name)
