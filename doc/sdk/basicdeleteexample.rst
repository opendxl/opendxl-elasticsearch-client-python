Basic Delete Example
====================

This sample deletes a document from an Elasticsearch server via the
Elasticsearch ``Delete`` API and displays the results of the delete request.

For more information on the Elasticsearch ``Delete`` API, see the
`Elasticsearch Python Delete API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.delete>`__
and `Elasticsearch REST Delete API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-delete.html>`__
documentation.

Prerequisites
*************

* The samples configuration step has been completed (see :doc:`sampleconfig`).
* The Elasticsearch API DXL service is running (see
  `Elasticsearch DXL Service <https://github.com/opendxl/opendxl-elasticsearch-service-python>`__).
* In order to enable the use of the ``delete`` API, the API name needs to be
  listed in the ``apiNames`` setting under the ``[General]`` section in the
  "dxlelasticsearchservice.config" file that the service uses:

    .. code-block:: ini

        [General]
        apiNames=delete,...

  For more information on the configuration, see the
  `Elasticsearch DXL Python Service configuration documentation <https://opendxl.github.io/opendxl-elasticsearch-service-python/pydoc/configuration.html#elasticsearch-dxl-python-service-dxlelasticsearchservice-config>`__.
* Run through the steps in the :doc:`basicindexexample`
  to store a document to Elasticsearch. This example will delete the stored
  document.

Running
*******

To run this sample execute the ``sample/basic/basic_delete_example.py`` script
as follows:

    .. code-block:: shell

        python sample/basic/basic_delete_example.py

If the document was previously stored via running the :doc:`basicindexexample`,
the output should appear similar to the following:

    .. code-block:: shell

        Response from delete:
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
            "found": true,
            "result": "deleted"
        }

If the document to be deleted does not exist on the Elasticsearch server at the
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
                # Invoke the delete method
                resp_dict = client.delete(
                    index=DOCUMENT_INDEX,
                    doc_type=DOCUMENT_TYPE,
                    id=DOCUMENT_ID)

                # Print out the response (convert dictionary to JSON for pretty
                # printing)
                print("Response from delete:\n{0}".format(
                    MessageUtils.dict_to_json(resp_dict, pretty_print=True)))
            except NotFoundError:
                print("Requested document was not found on the server")


Once a connection is established to the DXL fabric, a
:class:`dxlelasticsearchclient.client.ElasticsearchClient` instance is created
which will be used to invoke remote commands on the Elasticsearch DXL service.

Next, the :meth:`dxlelasticsearchclient.client.ElasticsearchClient.delete`
method is invoked with the ``index``, type (``doc_type``), and ``id`` of the
document to delete.

From the
`Elasticsearch Python Delete API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.delete>`_
documentation:

    `"Delete a typed JSON document from a specific index based on its id."`

If the document to be deleted does not exist on the Elasticsearch server at the
time the sample is run, the ``delete`` method will raise an
:class:`elasticsearch.exceptions.NotFoundError` exception. In this case, the
sample catches the exception, displays an error message, and exits.

If the document to be deleted does exist on the Elasticsearch server at the
time the sample is run, the final step is to display the contents of the
returned dictionary (``dict``) which contains the results of the attempt to
delete the document.
