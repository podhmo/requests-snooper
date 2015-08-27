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
