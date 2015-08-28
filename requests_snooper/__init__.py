# -*- coding:utf-8 -*-
import logging
from functools import wraps
from requests.sessions import Session

logger = logging.getLogger(__name__)


class OnionSession(Session):
    def __init__(self, middlewares):
        super(OnionSession, self).__init__()
        self.middlewares = middlewares

    def create_response(self, context, request):
        args = context["_args"]
        kwargs = {k: context[k] for k in context["_keys"]}
        return super(OnionSession, self).send(request, *args, **kwargs)

    def send(self, request, *args, **kwargs):
        context = {}
        context["_args"] = args
        context["_keys"] = list(kwargs.keys())
        context.update(kwargs)

        closure = self.create_response
        for m in self.middlewares:
            closure = m(closure)
        return closure(context, request)


def middlewarefy(fn):
    @wraps(fn)
    def middleware(closure):
        return lambda context, request: fn(closure)(context, request)
    return middleware

patched = False


def activate_monkey_patch(middlewares, session_factory=OnionSession):
    global patched
    if patched:
        return
    patched = True

    import requests.api

    def request(method, url, **kwargs):
        session = session_factory(middlewares)
        return session.request(method=method, url=url, **kwargs)
    requests.api.request = request
    requests.session = session_factory
