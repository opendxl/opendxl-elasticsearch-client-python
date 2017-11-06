import sys

import elasticsearch.exceptions

from dxlclient.message import Message, Request
from dxlbootstrap.util import MessageUtils
from dxlbootstrap.client import Client


class _ElasticsearchErrorType(object):
    def __init__(self, name):
        self.__name__ = name


class _ElasticsearchError(object):
    def __init__(self, error_type, error_message):
        self._error_type = error_type
        self._error_message = error_message

    def __getattribute__(self, name):
        if name == "__class__":
            return self._error_type
        else:
            return super(_ElasticsearchError, self).__getattribute__(name)

    def __str__(self):
        return self._error_message


class ElasticsearchClient(Client):
    """
    The "OpenDXL Elasticsearch Client" client wrapper class.
    """

    _SERVICE_TYPE = "/opendxl-elasticsearch/service/elasticsearch-api"

    _REQ_TOPIC_DELETE = "delete"
    _REQ_TOPIC_GET = "get"
    _REQ_TOPIC_INDEX = "index"
    _REQ_TOPIC_UPDATE = "update"

    _PARAM_BODY = "body"
    _PARAM_DOC_TYPE = "doc_type"
    _PARAM_ID = "id"
    _PARAM_INDEX = "index"

    _ELASTICSEARCH_EXCEPTIONS_MODULE = "elasticsearch.exceptions"
    _ELASTICSEARCH_EXCEPTIONS = \
        sys.modules[_ELASTICSEARCH_EXCEPTIONS_MODULE].__dict__

    def __init__(self, dxl_client, elasticsearch_service_unique_id=None):
        """
        Constructor parameters:

        :param dxl_client: The DXL client to use for communication with the
            fabric
        """
        super(ElasticsearchClient, self).__init__(dxl_client)
        self._dxl_client = dxl_client
        self._elasticsearch_service_unique_id = elasticsearch_service_unique_id

    def delete(self, index, doc_type, id, **kwargs):
        kwargs[self._PARAM_INDEX] = index
        kwargs[self._PARAM_DOC_TYPE] = doc_type
        kwargs[self._PARAM_ID] = id

        return self._invoke_service(self._REQ_TOPIC_DELETE, kwargs)

    def get(self, index, doc_type, id, **kwargs):
        kwargs[self._PARAM_INDEX] = index
        kwargs[self._PARAM_DOC_TYPE] = doc_type
        kwargs[self._PARAM_ID] = id

        return self._invoke_service(self._REQ_TOPIC_GET, kwargs)

    def index(self, index, doc_type, body, id=None, **kwargs):
        kwargs[self._PARAM_INDEX] = index
        kwargs[self._PARAM_DOC_TYPE] = doc_type
        kwargs[self._PARAM_BODY] = body
        kwargs[self._PARAM_ID] = id

        return self._invoke_service(self._REQ_TOPIC_INDEX, kwargs)

    def update(self, index, doc_type, id, body=None, **kwargs):
        kwargs[self._PARAM_INDEX] = index
        kwargs[self._PARAM_DOC_TYPE] = doc_type
        kwargs[self._PARAM_ID] = id
        kwargs[self._PARAM_BODY] = body

        return self._invoke_service(self._REQ_TOPIC_UPDATE, kwargs)

    def _raise_exception_for_error_response(self, response_dict):
        if response_dict.get("module") != \
                self._ELASTICSEARCH_EXCEPTIONS_MODULE:
            raise ValueError("Unknown exception in response")

        exception_class = self._ELASTICSEARCH_EXCEPTIONS.get(
            response_dict.get("class"))
        if exception_class:
            exception_data = response_dict.get("data")
            if exception_data and \
                    issubclass(exception_class,
                               elasticsearch.TransportError):
                info = exception_data.get("info")
                info_class = info.get("class")
                if info_class:
                    info = _ElasticsearchError(
                        _ElasticsearchErrorType(info_class),
                        info.get("error"))
                exception = exception_class(
                    exception_data.get("status_code"),
                    exception_data.get("error"),
                    info)
            else:
                exception = exception_class()
            raise exception
        else:
            raise ValueError("Unknown class in response")

    def _invoke_service(self, topic, request_dict):
        """
        """
        # Create the DXL request message
        request = Request("{}{}/{}".format(
            self._SERVICE_TYPE,
            "/{}".format(self._elasticsearch_service_unique_id)
            if self._elasticsearch_service_unique_id else "",
            topic))
    
        # Set the payload on the request message (Python dictionary to JSON
        # payload)
        MessageUtils.dict_to_json_payload(request, request_dict)
    
        # Perform a synchronous DXL request
        response = self._dxl_client.sync_request(request,
                                                 timeout=self.response_timeout)

        if response.message_type == Message.MESSAGE_TYPE_ERROR:
            try:
                self._raise_exception_for_error_response(
                    MessageUtils.json_payload_to_dict(response))
            except ValueError:
                raise Exception("Error: {} ({})".format(
                    response.error_message,
                    str(response.error_code)))

        # Convert the JSON payload in the DXL response message to a Python
        # dictionary and return it.
        return MessageUtils.json_payload_to_dict(response)
