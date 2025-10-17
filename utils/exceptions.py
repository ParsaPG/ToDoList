class NotFoundError(Exception):
    default_message = "Requested resource was not found."


class LimitError(Exception):
    default_message = "Resource limit reached."


class ValidationError(Exception):
    default_message = "Invalid input."