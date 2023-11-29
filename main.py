"""
    Main module, initializes a FastAPI object and starts uvicorn server
    Provides logging mechanism using middleware feature
"""
# Built-in packages
from datetime import datetime
# 3rd party packages
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
import uvicorn
# Project packages
from endpoints import router_top, router_user
from utils.logging import log_to_json
from data_models import RequestLog


app = FastAPI(title="Anime Database")

app.include_router(router_top)
app.include_router(router_user)


@app.middleware("http")
async def request_logging(request: Request, call_next):
    """
    Logs request and response related data into a JSON file
    :param request: Request object
    :param call_next: Calls endpoint functions, passes request object and gets response
    :return: Response to the end user
    """
    request_log = RequestLog()

    request_log.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    request_log.client_ip = request.client.host
    request_log.client_port = request.client.port
    request_log.url = str(request.url)
    request_log.method = request.method
    request_log.user_agent = request.headers.get("user-agent")
    request_log.username = request.headers.get("x-username")
    request_log.user_key = request.headers.get("x-key")

    response: StreamingResponse = await call_next(request)

    request_log.response_code = response.status_code

    log_to_json("./request_logs/request_logs.json", request_log.model_dump())

    return response


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8081)
