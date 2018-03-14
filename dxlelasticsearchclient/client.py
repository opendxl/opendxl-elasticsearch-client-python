from __future__ import absolute_import
import sys

import elasticsearch.exceptions

from dxlclient.message import Message, Request
from dxlbootstrap.util import MessageUtils
from dxlbootstrap.client import Client


class ElasticsearchClient(Client):
    """
    The "Elasticsearch DXL Python Client Library" client wrapper class.
    """

    #: The DXL service type for the Elasticsearch API.
    _SERVICE_TYPE = "/opendxl-elasticsearch/service/elasticsearch-api"

    #: The DXL topic fragment for the Elasticsearch "delete" method.
    _REQ_TOPIC_DELETE = "delete"
    #: The DXL topic fragment for the Elasticsearch "get" method.
    _REQ_TOPIC_GET = "get"
    #: The DXL topic fragment for the Elasticsearch "index" method.
    _REQ_TOPIC_INDEX = "index"
    #: The DXL topic fragment for the Elasticsearch "update" method.
    _REQ_TOPIC_UPDATE = "update"

    #: The document body parameter.
    _PARAM_BODY = "body"
    #: The document type parameter.
    _PARAM_DOC_TYPE = "doc_type"
    #: The document id parameter.
    _PARAM_ID = "id"
    #: The document index parameter.
    _PARAM_INDEX = "index"

    # Reference to the available exception classes in the elasticsearch
    # Python library - used when converting error responses into exceptions.
    _ELASTICSEARCH_EXCEPTIONS_MODULE = "elasticsearch.exceptions"
    _ELASTICSEARCH_EXCEPTIONS = \
        sys.modules[_ELASTICSEARCH_EXCEPTIONS_MODULE].__dict__

    def __init__(self, dxl_client, elasticsearch_service_unique_id=None):
        """
        Constructor parameters:

        :param dxlclient.client.DxlClient dxl_client: The DXL client to use for
            communication with the fabric.
        :param str elasticsearch_service_unique_id: Unique id to use as part
            of the request topic names for the Elasticsearch DXL service.
        """
        super(ElasticsearchClient, self).__init__(dxl_client)
        self._dxl_client = dxl_client
        self._elasticsearch_service_unique_id = elasticsearch_service_unique_id

    def delete(self, index, doc_type, id, **kwargs): # pylint: disable=invalid-name,redefined-builtin
        """
        Deletes a typed JSON document from a specific index based on its id.
        See the `Elasticsearch Python Delete API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.delete>`__
        and `Elasticsearch REST Delete API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-delete.html>`__
        documentation for more information on the full set of available
        parameters and data format.

        :param str index: Name of the index.
        :param str doc_type: Type of the document.
        :param str id: ID of the document.
        :param dict kwargs: Dictionary of additional parameters to pass along
            to the Elasticsearch Python API.
        :return: Result of the deletion attempt.
        :rtype: dict
        :raises elasticsearch.exceptions.NotFoundError: If the document cannot
            be found.
        """
        kwargs[self._PARAM_INDEX] = index
        kwargs[self._PARAM_DOC_TYPE] = doc_type
        kwargs[self._PARAM_ID] = id

        return self._invoke_service(self._REQ_TOPIC_DELETE, kwargs)

    def get(self, index, doc_type, id, **kwargs): # pylint: disable=invalid-name,redefined-builtin
        """
        Gets a typed JSON document from a specific index based on its id.
        See the `Elasticsearch Python Get API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.get>`__
        and `Elasticsearch REST Get API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html>`__
        documentation for more information on the full set of available
        parameters and data format.

        :param str index: Name of the index.
        :param str doc_type: Type of the document.
        :param str id: ID of the document.
        :param dict kwargs: Dictionary of additional parameters to pass along
            to the Elasticsearch Python API.
        :return: Result of the get attempt.
        :rtype: dict
        :raises elasticsearch.exceptions.NotFoundError: If the document cannot
            be found.
        """
        kwargs[self._PARAM_INDEX] = index
        kwargs[self._PARAM_DOC_TYPE] = doc_type
        kwargs[self._PARAM_ID] = id

        return self._invoke_service(self._REQ_TOPIC_GET, kwargs)

    def index(self, index, doc_type, body, id=None, **kwargs): # pylint: disable=invalid-name,redefined-builtin
        """
        Adds or updates a typed JSON document from a specific index based on
        its id. See the `Elasticsearch Python Index API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index>`__
        and `Elasticsearch REST Index API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html>`__
        documentation for more information on the full set of available
        parameters and data format.

        :param str index: Name of the index.
        :param str doc_type: Type of the document.
        :param dict body: The document.
        :param str id: ID of the document.
        :param dict kwargs: Dictionary of additional parameters to pass along
            to the Elasticsearch Python API.
        :return: Result of the index attempt.
        :rtype: dict
        :raises elasticsearch.exceptions.NotFoundError: If the document cannot
            be found.
        """
        kwargs[self._PARAM_INDEX] = index
        kwargs[self._PARAM_DOC_TYPE] = doc_type
        kwargs[self._PARAM_BODY] = body
        kwargs[self._PARAM_ID] = id

        return self._invoke_service(self._REQ_TOPIC_INDEX, kwargs)

    def update(self, index, doc_type, id, body=None, **kwargs): # pylint: disable=invalid-name,redefined-builtin
        """
        Update a document based on a script or partial data provided. See the
        `Elasticsearch Python Update API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.update>`__
        and `Elasticsearch REST Update API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html>`__
        documentation for more information on the full set of available
        parameters and data format.

        :param str index: Name of the index.
        :param str doc_type: Type of the document.
        :param str id: ID of the document.
        :param dict body: The request definition using either script or partial
            doc.
        :param dict kwargs: Dictionary of additional parameters to pass along
            to the Elasticsearch Python API.
        :return: Result of the update attempt.
        :rtype: dict
        :raises elasticsearch.exceptions.NotFoundError: If the document cannot
            be found.
        """
        kwargs[self._PARAM_INDEX] = index
        kwargs[self._PARAM_DOC_TYPE] = doc_type
        kwargs[self._PARAM_ID] = id
        kwargs[self._PARAM_BODY] = body

        return self._invoke_service(self._REQ_TOPIC_UPDATE, kwargs)

    def _raise_exception_for_error_response(self, response_dict):
        """
        Raise an exception based on the dictionary content received in the
        payload for a DXL 'dxlclient.message.ErrorResponse'.

        :param dict response_dict: The error response payload.
        :raises Exception: An appropriate exception for the payload. An
            exception will be raised from one of the classes in
            the 'elasticsearch.exceptions' module, if possible. If not, a
            more generic ValueError is raised.
        """
        if response_dict.get("module") != \
                self._ELASTICSEARCH_EXCEPTIONS_MODULE:
            raise ValueError("Unknown exception in response")

        exception_class = self._ELASTICSEARCH_EXCEPTIONS.get(
            response_dict.get("class"))
        if exception_class:
            # An exception class from the 'elasticsearch.exceptions' module
            # matches the error response payload
            exception_data = response_dict.get("data")
            if exception_data and \
                    issubclass(exception_class,
                               elasticsearch.TransportError):
                # Determine the parameters to use for constructing a
                # TransportError (or subclass)
                info = exception_data.get("info")
                # If the class element is present in the 'info' dictionary,
                # the original error on the server was an Exception object.
                # In this case, a dummy _ElasticsearchNestedException instance
                # which references the name and error message is re-constructed
                # rather than the actual exception class, which may not be
                # resolvable in the client code.
                info_class = info.get("class")
                if info_class:
                    info = _ElasticsearchNestedException(
                        _ElasticsearchNestedExceptionType(info_class),
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

    def _invoke_service(self, request_method, request_dict):
        """
        Invokes a request method on the Elasticsearch DXL service.

        :param str request_method: The request method to append to the
            topic for the request.
        :param dict request_dict: Dictionary containing request information.
        :return: Results of the service invocation.
        :rtype: dict
        """
        if self._elasticsearch_service_unique_id:
            request_service_id = "/{}".format(
                self._elasticsearch_service_unique_id)
        else:
            request_service_id = ""

        # Create the DXL request message.
        request = Request("{}{}/{}".format(
            self._SERVICE_TYPE,
            request_service_id,
            request_method))

        # Set the payload on the request message (Python dictionary to JSON
        # payload).
        MessageUtils.dict_to_json_payload(request, request_dict)

        # Perform a synchronous DXL request.
        response = self._dxl_client.sync_request(request,
                                                 timeout=self.response_timeout)

        if response.message_type == Message.MESSAGE_TYPE_ERROR:
            try:
                self._raise_exception_for_error_response(
                    MessageUtils.json_payload_to_dict(response))
            except ValueError:
                # If an appropriate exception cannot be constructed from the
                # error response data, raise a more generic Exception as a
                # fallback.
                raise Exception("Error: {} ({})".format(
                    response.error_message,
                    str(response.error_code)))

        # Convert the JSON payload in the DXL response message to a Python
        # dictionary and return it.
        return MessageUtils.json_payload_to_dict(response)


class _ElasticsearchNestedExceptionType(object):
    """
    Class used to hold the name of a nested (inner) exception which can be
    embedded in the data of one of the top-level exceptions from the
    'elasticsearch.exceptions' module.

    :param str name: Name of the nested exception class
    """
    def __init__(self, name):
        self.__name__ = name


class _ElasticsearchNestedException(object):
    """
    Class holding the details of a nested (inner) exception which can be
    embedded in the data of one of the top-level exceptions from the
    'elasticsearch.exceptions' module.
    """
    def __init__(self, error_type, error_message):
        """
        Constructor parameters:

        :param _ElasticsearchNestedExceptionType error_type: Object holding
            metadata (for example, the class name) of the nested exception.
        :param str error_message: String description of the error
        """
        self._error_type = error_type
        self._error_message = error_message

    def __getattribute__(self, name):
        if name == "__class__":
            return_value = self._error_type
        else:
            return_value = super(_ElasticsearchNestedException,
                                 self).__getattribute__(name)
        return return_value

    def __str__(self):
        return self._error_message
