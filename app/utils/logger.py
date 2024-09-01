
import logging
from flask import request, g
from datetime import datetime

logging.basicConfig(filename='request_log.txt',
                    level=logging.INFO, format='%(asctime)s - %(message)s')


def log_request_info():
    g.start_time = datetime.now()
    request_info = {
        'method': request.method,
        'url': request.url,
        'headers': dict(request.headers),
        'body': request.get_data(as_text=True),
    }
    logging.info(f"Request: {request_info}")


def log_response_info(response):
    duration = datetime.now() - g.start_time
    response_info = {
        'status_code': response.status_code,
        'duration': str(duration),
    }
    logging.info(f"Response: {response_info}")
    return response
