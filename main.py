import json, time
from requests import session
from valclient.client import Client
print('Valorant Agent Yoinker originally by https://github.com/deadly')
print('updated by : https://github.com/Imu-D-sama')
print('ver 0.2')
valid = False
agents = {}
seenMatches = []

with open('data.json', 'r') as f:
    data = json.load(f)
    ranBefore = data['ran']
    agents = data['agents']
    region = data['region']
    
if (ranBefore == False):
    region = input("Enter your region: ").lower()
    client = Client(region=region)
    client.activate()

    with open('data.json', 'w') as f:
            data['ran'] = True
            data['region'] = region
            json.dump(data, f, indent=4)
else:
    client = Client(region=region)
    client.activate()

while valid == False:
            try:
                preferredAgent = input(f"Preferred Agent or dodge the match: ").lower()
                if (preferredAgent in agents.keys() or preferredAgent == "dodge"):
                    valid = True    
                else:
                    print("Invalid Agent")
            except Exception as e:
                print("Input Error")          
print("Waiting for Agent Select")

while True:
    try:
        sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
        if((preferredAgent == "dodge") and (sessionState == "PREGAME") and (client.pregame_fetch_match()['ID'] not in seenMatches)):
            print('Agent Select Screen Found')
            client.pregame_quit_match()
            seenMatches.append(client.pregame_fetch_match()['ID'])
            print('Successfully dodged the Match')
        elif ((sessionState == "PREGAME") and (client.pregame_fetch_match()['ID'] not in seenMatches) and (preferredAgent in agents.keys())):
            print('Agent Select Screen Found')
            client.pregame_select_character(agents[preferredAgent])
            client.pregame_lock_character(agents[preferredAgent])
            seenMatches.append(client.pregame_fetch_match()['ID'])
            print('Successfully Locked ' + preferredAgent.capitalize())
    except Exception as e:
        print('', end='') 
