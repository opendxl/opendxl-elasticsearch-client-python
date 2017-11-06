import os
import sys

from dxlbootstrap.util import MessageUtils
from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient

root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir + "/../..")
sys.path.append(root_dir + "/..")

from dxlelasticsearchclient.client import ElasticsearchClient

# Import common logging and configuration
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

DOCUMENT_INDEX = "opendxl-elasticsearch-client-examples"
DOCUMENT_TYPE = "basic-example-doc"
DOCUMENT_ID = "12345"

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as dxl_client:

    # Connect to the fabric
    dxl_client.connect()

    logger.info("Connected to DXL fabric.")

    # Create client wrapper
    client = ElasticsearchClient(dxl_client)

    # Invoke the example method
    resp_dict = client.update(
        index=DOCUMENT_INDEX,
        doc_type=DOCUMENT_TYPE,
        id=DOCUMENT_ID,
        body={"doc": {"source": "Basic Update Example"}})

    # Print out the response (convert dictionary to JSON for pretty printing)
    print "Response from update:\n{0}".format(
        MessageUtils.dict_to_json(resp_dict, pretty_print=True))

    # Invoke the example method
    resp_dict = client.get(
        index=DOCUMENT_INDEX,
        doc_type=DOCUMENT_TYPE,
        id=DOCUMENT_ID)

    print "Response from get:\n{0}".format(
        MessageUtils.dict_to_json(resp_dict, pretty_print=True))
