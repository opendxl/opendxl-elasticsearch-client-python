Basic Index Example
===================

This sample stores a document to an Elasticsearch server via the Elasticsearch
``Index`` API. The sample then retrieves the contents of the stored document
via a call to the Elasticsearch ``Get`` API. The sample displays the results of
the ``Index`` and ``Get`` calls.

For more information on the Elasticsearch ``Index`` API, see the
`Elasticsearch Python Index API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index>`__
and `Elasticsearch REST Index API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html>`__
documentation.

Prerequisites
*************

* The samples configuration step has been completed (see :doc:`sampleconfig`).
* The Elasticsearch API DXL service is running (see
  `Elasticsearch DXL Service <https://github.com/opendxl/opendxl-elasticsearch-service-python>`__).
* In order to enable the use of the ``index`` and ``get`` APIs, both API names
  need to be listed in the ``apiNames`` setting under the ``[General]`` section
  in the "dxlelasticsearchservice.config" file that the service uses:

    .. code-block:: ini

        [General]
        apiNames=index,get,...

  For more information on the configuration, see the
  `Elasticsearch DXL Python Service configuration documentation <https://opendxl.github.io/opendxl-elasticsearch-service-python/pydoc/configuration.html#elasticsearch-dxl-python-service-dxlelasticsearchservice-config>`__.

Running
*******

To run this sample execute the ``sample/basic/basic_index_example.py`` script
as follows:

    .. code-block:: shell

        python sample/basic/basic_index_example.py

The output should appear similar to the following:

    .. code-block:: shell

        Response from index:
        {
            "_id": "12345",
            "_index": "opendxl-elasticsearch-client-examples",
            "_shards": {
                "failed": 0,
                "successful": 1,
                "total": 2
            },
            "_type": "basic-example-doc",
            "_version": 1,
            "created": true,
            "result": "created"
        }
        Response from get:
        {
            "_id": "12345",
            "_index": "opendxl-elasticsearch-client-examples",
            "_source": {
                "message": "Hello from OpenDXL",
                "source": "Basic Index Example"
            },
            "_type": "basic-example-doc",
            "_version": 1,
            "found": true
        }

Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

        # Create the client
        with DxlClient(config) as dxl_client:

            # Connect to the fabric
            dxl_client.connect()

            logger.info("Connected to DXL fabric.")

            # Create client wrapper
            client = ElasticsearchClient(dxl_client)

            # Invoke the index method
            resp_dict = client.index(
                index=DOCUMENT_INDEX,
                doc_type=DOCUMENT_TYPE,
                id=DOCUMENT_ID,
                body={"message": "Hello from OpenDXL",
                      "source": "Basic Index Example"})

            # Print out the response (convert dictionary to JSON for pretty printing)
            print("Response from index:\n{0}".format(
                MessageUtils.dict_to_json(resp_dict, pretty_print=True)))

            # Invoke the get method
            resp_dict = client.get(
                index=DOCUMENT_INDEX,
                doc_type=DOCUMENT_TYPE,
                id=DOCUMENT_ID)

            # Print out the response (convert dictionary to JSON for pretty printing)
            print("Response from get:\n{0}".format(
                MessageUtils.dict_to_json(resp_dict, pretty_print=True)))


Once a connection is established to the DXL fabric, a
:class:`dxlelasticsearchclient.client.ElasticsearchClient` instance is created
which will be used to invoke remote commands on the Elasticsearch DXL service.

Next, the :meth:`dxlelasticsearchclient.client.ElasticsearchClient.index`
method is invoked with the ``index``, type (``doc_type``), and ``id`` at which
to store the document. The call also includes a ``dict`` representing the
``body`` of the document to store.

From the
`Elasticsearch Python Index API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index>`_
documentation:

    `"Adds or updates a typed JSON document in a specific index, making it
    searchable."`

The next step is to display the contents of the returned dictionary (``dict``)
which contains the results of the attempt to store the document.

To confirm that the document was stored properly, the
:meth:`dxlelasticsearchclient.client.ElasticsearchClient.get` method is invoked
to retrieve the information stored for the document. The method is invoked with
the same ``index``, type (``doc_type``), and ``id`` of the document used in the
prior call to the ``index`` method.

From the
`Elasticsearch Python Get API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.get>`_
documentation:

    `"Get a typed JSON document from the index based on its id."`

The final step is to display the contents of the returned dictionary (``dict``)
which contains information for the stored document.
