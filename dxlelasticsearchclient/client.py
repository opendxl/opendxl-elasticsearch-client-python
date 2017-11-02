from dxlclient.message import Request
from dxlbootstrap.util import MessageUtils
from dxlbootstrap.client import Client


class ElasticsearchClient(Client):
    """
    The "OpenDXL Elasticsearch Client" client wrapper class.
    """

    _SERVICE_TYPE = "/opendxl-elasticsearch/service/elasticsearch-api"

    def __init__(self, dxl_client, elasticsearch_service_unique_id):
        """
        Constructor parameters:

        :param dxl_client: The DXL client to use for communication with the fabric
        """
        super(ElasticsearchClient, self).__init__(dxl_client)
        self._dxl_client = dxl_client
        self._elasticsearch_service_unique_id = elasticsearch_service_unique_id

    def get(self, index, doc_type, id, params=None, **kwargs):
        kwargs["index"] = index
        kwargs["doc_type"] = doc_type
        kwargs["id"] = id
        kwargs["params"] = params if params else {}

        return self._invoke_service("get", kwargs)

    def index(self, index, doc_type, body, id=None, params=None, **kwargs):
        kwargs["index"] = index
        kwargs["doc_type"] = doc_type
        kwargs["body"] = body
        kwargs["id"] = id
        kwargs["params"] = params if params else {}

        return self._invoke_service("index", kwargs)

    def _invoke_service(self, topic, request_dict):
        """
        """
        # Create the DXL request message
        request = Request("{}/{}/{}".format(
            self._SERVICE_TYPE,
            self._elasticsearch_service_unique_id,
            topic))
    
        # Set the payload on the request message (Python dictionary to JSON
        # payload)
        MessageUtils.dict_to_json_payload(request, request_dict)
    
        # Perform a synchronous DXL request
        response = self._dxl_sync_request(request)
    
        # Convert the JSON payload in the DXL response message to a Python
        # dictionary and return it.
        return MessageUtils.json_payload_to_dict(response)


