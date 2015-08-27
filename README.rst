requests-snooper
========================================

wsgi middleware like function on http requests.


the way of using
----------------------------------------

.. code-block:: python

  import requests
  from requests_snooper import middlewarefy, activate_monkey_patch


  @middlewarefy
  def hello(create_response):
      def _hello(context, request):
          print(">>> request.url={}".format(request.url))
          response = create_response(context, request)
          print("<<< response.core={}".format(response.status_code))
          return response
      return _hello

  activate_monkey_patch([hello])
  response = requests.get("http://github.com/podhmo/requests-snooper")
  print(response)


output

::

  >>> request.url=http://github.com/podhmo/requests-snooper
  >>> request.url=https://github.com/podhmo/requests-snooper
  <<< response.core=404
  <<< response.core=404
  <Response [404]>

