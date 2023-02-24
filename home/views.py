import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . models import Messages
import requests

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'GET':
        print('Post data....')
        print(request.GET.get('hub.challenge'))
        x = request.GET.get('hub.challenge')
        return HttpResponse(x,status=200)
    else:
        data = json.loads(request.body)
        print(data)
        # print(data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'])

        try:
            msg_id = data['entry'][0]['changes'][0]['value']['messages'][0]['id']
            msg = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            name = data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
            number = data['entry'][0]['changes'][0]['value']['metadata']['display_phone_number']
            time_stamp = data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
            # print(msg_id)

            qs = Messages(msg_id=msg_id,msg = msg,time_stamp=time_stamp,display_name=name,display_phone=number)
            qs.save()
        except:
            msg_id = data['entry'][0]['changes'][0]['value']['statuses'][0]['id']
            # msg = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            status = data['entry'][0]['changes'][0]['value']['statuses'][0]['status']
            # name = data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
            number = data['entry'][0]['changes'][0]['value']['metadata']['display_phone_number']
            time_stamp = data['entry'][0]['changes'][0]['value']['statuses'][0]['timestamp']

            if Messages.objects.filter(msg_id=msg_id).exists():
                qs = Messages.objects.get(msg_id=msg_id)
                qs.status = status
                qs.time_stamp=time_stamp
                
            else:
                qs = Messages(msg_id=msg_id,status=status,time_stamp=time_stamp,display_phone=number)
            qs.save()
        
        
    return HttpResponse(status=200)

    '''
      https://graph.facebook.com/v14.0/104320902436909/messages `
  -H 'Authorization: Bearer EAAIUBRFiZCP8BAIYJlh0R6s8RXXR5ZBrZC27NmJ49ZAfb4sSgDV97nthZChbM9LeDFHSgXqtDJf56RaoS95vUMzSdmZCatsFrUD0BXIGRZC3rHXjt3JXe0eXzLzJqOJUySA6eQwToBK7yTyn7KmaFlO6R79KwYJyie8U1ZBa2SpspqCLcQFaMfckZAOfzNh7xf4Y7LbbHlFtVgDndBZCgNZCRWM' `
  -H 'Content-Type: application/json' `
  -d '{ \"messaging_product\": \"whatsapp\", \"to\": \"918434355347\", \"type\": \"template\", \"template\": { \"name\": \"hello_world\", \"language\": { \"code\": \"en_US\" } } }'
    
    '''

def send_wa_msg(request):
    base_url = "https://graph.facebook.com/v15.0/111081381911326/messages"

    data = {
        "messaging_product":"whatsapp",
        "to":"918827290484",
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en",
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": "Srejus"
                        },
                        {
                            "type": "text",
                            "text": "Ram"
                        },
                        {
                            "type": "text",
                            "text": "10"
                        },
                        {
                            "type": "text",
                            "text": "https://pay.enalo.in"
                        },
                        {
                            "type": "text",
                            "text": "--"
                        },
                        {
                            "type": "text",
                            "text": "--"
                        },
                        
                        
                    ] 
                },

                {
                            "type": "button",
                            "sub_type":"url",
                            "index": "0",
                            "parameters":[
                                {
                                    "type":"payload",
                                    "payload":"202200265"
                                }
                            ]
                        },
                
            ]
        }
    }


    API_TOKEN = "EAAUZA6S7SKDkBAGc7orZAznCZA7PijxkSRU3XNZAk3cUx1d2E0bTNSZAKzOzQmEso4LebVnZBxyYXuqe0bAATOVPe0c428fVZAd5NoqYddNRo3M8sDQpQ4HpkeieG5Ek9mIg29nLdXzD8WiKDaALlCn4LZBLbue9Pn2Mw3V0nJ2XAP6jo4E2lJ8Qioew1kW9XhiwiOzuirOo0AZDZD"

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    r = requests.post(base_url,data=json.dumps(data),headers=headers)
    data = r.json()

    try:
        msg_id = data['messages'][0]['id']
        number = data['contacts'][0]['input']

        qs = Messages(msg_id = msg_id,display_phone=number)
        qs.save()
    except:
        print(data)

    return HttpResponse(status=200)