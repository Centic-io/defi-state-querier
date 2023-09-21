# SOFTWARE.


import threading
from web3._utils.request import make_post_request
from urllib.parse import urlparse

from web3 import HTTPProvider, WebsocketProvider

DEFAULT_TIMEOUT = 60


class ThreadLocalProxy:
    def __init__(self, delegate_factory):
        self._thread_local = threading.local()
        self._delegate_factory = delegate_factory

    def __getattr__(self, name):
        return getattr(self._get_thread_local_delegate(), name)

    def _get_thread_local_delegate(self):
        if getattr(self._thread_local, '_delegate', None) is None:
            self._thread_local._delegate = self._delegate_factory()
        return self._thread_local._delegate


def get_provider_from_uri(uri_string, timeout=DEFAULT_TIMEOUT, batch=False):
    uri = urlparse(uri_string)
    if uri.scheme == 'http' or uri.scheme == 'https':
        request_kwargs = {'timeout': timeout}
        if batch:
            return BatchHTTPProvider(uri_string, request_kwargs=request_kwargs)
        else:
            return HTTPProvider(uri_string, request_kwargs=request_kwargs)
    elif uri.scheme == "wss" or uri.scheme == "ws":
        websocket_kwargs = {'timeout': timeout}
        if batch:
            return BatchWebsocketProvider(uri_string, websocket_kwargs=websocket_kwargs)
        else:
            return WebsocketProvider(uri_string, websocket_kwargs=websocket_kwargs)
    else:
        raise ValueError('Unknown uri scheme {}'.format(uri_string))


# Mostly copied from web3.py/providers/rpc.py. Supports batch requests.
# Will be removed once batch feature is added to web3.py https://github.com/ethereum/web3.py/issues/832
class BatchHTTPProvider(HTTPProvider):

    def make_batch_request(self, text):
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                          self.endpoint_uri, text)
        request_data = text.encode('utf-8')
        raw_response = make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Request: %s, Response: %s",
                          self.endpoint_uri, text, response)
        return response


class BatchWebsocketProvider(WebsocketProvider):

    def make_batch_request(self, text):
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                          self.endpoint_uri, text)
        request_data = text.encode('utf-8')
        raw_response = make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Request: %s, Response: %s",
                          self.endpoint_uri, text, response)
        return response
