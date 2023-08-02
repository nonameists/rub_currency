from rest_framework.exceptions import APIException


class DateNotFoundException(APIException):
    """Custom exception hold wrong date from cbrf."""
    status_code = 404
    default_detail = "Date not found."

