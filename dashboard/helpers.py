from accounts.models import OwnBrokersCredentials
from fyers_api import fyersModel


def get_fyers_profile(request, data):
    api_key = OwnBrokersCredentials.objects.filter(broker__short_title='fyers').first()
    fyers = fyersModel.FyersModel(client_id=api_key.api_key, token=request.COOKIES.get('access_token'))

    response = fyers.get_profile()
    print(response)

    data['name'] = response.get('data').get('name')
    data['id'] = response.get('data').get('fy_id')
    data['mobile_number'] = response.get('data').get('mobile_number')
    data['email_id'] = response.get('data').get('email_id')