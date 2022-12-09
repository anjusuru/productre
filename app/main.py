from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.api_v1 import api
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware


description = """"

This is a dummy project

"""

tags = [
    {"name": "User", "description": "This is user related route"},
    {"name": "Product", "description": "This is product related route"},
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description=description,
    version="0.0.1",
    openapi_tags=tags,
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


# # Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )


app.include_router(api.router, prefix=settings.API_V1_STR)
