''''
def app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type','text/plain')]
    start_response(status, response_headers)
    return [b'Hello world!\n']
'''
import json
def app(environ, start_response):
    """Return body as JSON"""
    status = '200 OK'
    response_headers = [('Content-Type', 'application/json')]
    start_response(status, response_headers)

    message = {"environment" : f"{environ}"}

    body = json.dumps(message).encode("utf-8")
    return [body]
