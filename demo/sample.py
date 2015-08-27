import requests
from requests_snooper import middlewarefy, activate_monkey_patch


@middlewarefy
def capture(create_response):
    def _capture(context, request):
        print(">>> request.url={}".format(request.url))
        response = create_response(context, request)
        print("<<< response.code={}".format(response.status_code))
        return response
    return _capture

activate_monkey_patch([capture])
response = requests.get("http://github.com/podhmo/requests-snooper")
print(response)
