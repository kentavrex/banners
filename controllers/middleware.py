import logging

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware
from usecases.errors import NotFoundError, ValidationError


class HandleHTTPErrorsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except NotFoundError as e:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": str(e)})
        except ValidationError as e:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"error": str(e)})
        except Exception as e:
            logging.error(f"Error Type: {type(e)}")
            logging.error(str(e))
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal Server Error"}
            )
        return response


class CORSMiddlewareCustom(BaseHTTPMiddleware):
    _allow_methods = 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'
    _allow_headers = 'Accept, Accept-Language, Content-Type, Content-Language'

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS" and "access-control-request-method" in request.headers:
            return self.preflight_response(request_headers=request.headers)

        response = await call_next(request)

        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response.headers['Access-Control-Allow-Methods'] = self._allow_methods
        response.headers['Access-Control-Allow-Headers'] = self._allow_headers
        return response

    def preflight_response(self, request_headers):
        preflight_headers = {
            "Vary": "Origin",
            "Access-Control-Allow-Methods": self._allow_methods,
            "Access-Control-Max-Age": "600",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Origin": request_headers["origin"],
            "Access-Control-Allow-Headers": request_headers.get("access-control-request-headers", self._allow_headers)
        }

        return PlainTextResponse("OK", status_code=200, headers=preflight_headers)
