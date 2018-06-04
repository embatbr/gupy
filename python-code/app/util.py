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

