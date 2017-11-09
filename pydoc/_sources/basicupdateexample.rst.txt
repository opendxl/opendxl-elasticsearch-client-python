Basic Update Example
====================

This sample updates a document to an Elasticsearch server via the Elasticsearch
``Update`` API. The sample then retrieves the contents of the updated document
via a call to the Elasticsearch ``Get`` API. The sample displays the results of
the ``Update`` and ``Get`` calls.

For more information on the Elasticsearch ``Update`` API, see the
`Elasticsearch Python Update API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.update>`__
and `Elasticsearch REST Update API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html>`__
documentation.

Prerequisites
*************

* The samples configuration step has been completed (see :doc:`sampleconfig`).
* The Elasticsearch API DXL service is running (see
  `Elasticsearch DXL Service <https://github.com/opendxl/opendxl-elasticsearch-service-python>`__).
* In order to enable the use of the ``update`` and ``get`` APIs, both API names
  need to be listed in the ``apiNames`` setting under the ``[General]`` section
  in the "dxlelasticsearchservice.config" file that the service uses:

    .. code-block:: ini

        [General]
        apiNames=update,get,...

  For more information on the configuration, see the
  `Elasticsearch DXL Python Service configuration documentation <https://opendxl.github.io/opendxl-elasticsearch-service-python/pydoc/configuration.html#elasticsearch-dxl-python-service-dxlelasticsearchservice-config>`__.
* Run through the steps in the :doc:`basicindexexample`
  to store a document to Elasticsearch. This example will update the stored
  document.

Running
*******

To run this sample execute the ``sample/basic/basic_update_example.py`` script
as follows:

    .. code-block:: shell

        python sample/basic/basic_update_example.py

If the document was previously stored via running the :doc:`basicindexexample`,
the output should appear similar to the following:

    .. code-block:: shell

        Response from update:
        {
            "_id": "12345",
            "_index": "opendxl-elasticsearch-client-examples",
            "_shards": {
                "failed": 0,
                "successful": 2,
                "total": 2
            },
            "_type": "basic-example-doc",
            "_version": 2,
            "result": "updated"
        }
        Response from get:
        {
            "_id": "12345",
            "_index": "opendxl-elasticsearch-client-examples",
            "_source": {
                "message": "Hello from OpenDXL",
                "source": "Basic Update Example"
            },
            "_type": "basic-example-doc",
            "_version": 2,
            "found": true
        }

If the document to be updated does not exist on the Elasticsearch server at the
time the sample is run, the output should appear similar to the following:

    .. code-block:: shell

        Requested document was not found on the server

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

            try:
                # Invoke the update method
                resp_dict = client.update(
                    index=DOCUMENT_INDEX,
                    doc_type=DOCUMENT_TYPE,
                    id=DOCUMENT_ID,
                    body={"doc": {"source": "Basic Update Example"}})
            except NotFoundError:
                print("Requested document was not found on the server")
                sys.exit(1)

            # Print out the response (convert dictionary to JSON for pretty printing)
            print("Response from update:\n{0}".format(
                MessageUtils.dict_to_json(resp_dict, pretty_print=True)))

            # Invoke the get method
            resp_dict = client.get(
                index=DOCUMENT_INDEX,
                doc_type=DOCUMENT_TYPE,
                id=DOCUMENT_ID)

            print("Response from get:\n{0}".format(
                MessageUtils.dict_to_json(resp_dict, pretty_print=True)))


Once a connection is established to the DXL fabric, a
:class:`dxlelasticsearchclient.client.ElasticsearchClient` instance is created
which will be used to invoke remote commands on the Elasticsearch DXL service.

Next, the :meth:`dxlelasticsearchclient.client.ElasticsearchClient.update`
method is invoked with the ``index``, type (``doc_type``), and ``id`` of the
document to update. The call also includes a ``dict`` representing the portion
of the document ``body`` to update.

From the
`Elasticsearch Python Update API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.update>`_
documentation:

     `"Update a document based on a script or partial data provided."`

If the document to be updated does not exist on the Elasticsearch server at the
time the sample is run, the ``update`` method will raise an
:class:`elasticsearch.exceptions.NotFoundError` exception. In this case, the
sample catches the exception, displays an error message, and exits.

If the document to be updated does exist on the Elasticsearch server at the
time the sample is run, the next step is to display the contents of the
returned dictionary (``dict``) which contains the results of the attempt to
update the document.

To confirm that the document was updated properly, the
:meth:`dxlelasticsearchclient.client.ElasticsearchClient.get` method is invoked
to retrieve the information updated for the document. The method is invoked with
the same ``index``, type (``doc_type``), and ``id`` of the document used in the
prior call to the ``update`` method.

From the
`Elasticsearch Python Get API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.get>`_
documentation:

    `"Get a typed JSON document from the index based on its id."`

The final step is to display the contents of the returned dictionary (``dict``)
which contains information for the updated document.
