from rest_framework.response import Response
from rest_framework import status

class ResponseHandler:
    @staticmethod
    def success(data=None, message="Operation successful", status_code=status.HTTP_200_OK):
        """Returns a successful response."""
        response = {
            "status": True,
            "message": message,
            "response": "success",
        }
        if data:
            response["data"] = data
        return Response(response, status=status_code)

    @staticmethod
    def failure(message="An error occurred", status_code=status.HTTP_400_BAD_REQUEST, data=None):
        """Returns a failure response."""
        response = {
            "status": False,
            "message": message,
            "response": "fail",
        }
        if data:
            response["data"] = data
        return Response(response, status=status_code)

    @staticmethod
    def validation_error(errors, status_code=status.HTTP_400_BAD_REQUEST):
        """Returns a validation error response."""
        return Response(
            {
                "status": False,
                "message": "Validation errors occurred.",
                "response": "fail",
                "errors": errors
            },
            status=status_code
        )
    
