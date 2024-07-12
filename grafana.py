import requests

 
def get_teams(basic_auth, grafana_url):
    url = f"{grafana_url}/api/teams/search"
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def add_user_to_team(basic_auth, grafana_url, teamId, userId):
    url = f"{grafana_url}/api/teams/{teamId}/members"
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/json"
    }
    data = {
        "userId": userId
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"User {userId} add to team {teamId} successful")
    else:
        print(f"Failed add user to team: {response.status_code}, {response.text}")
    return response.json()

def add_user_to_org(basic_auth, grafana_url, org_id, user_email, role):
    url = f"{grafana_url}/api/orgs/{org_id}/users"
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/json"
    }
    data = {
        "loginOrEmail": user_email,
        "role": role
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def sync_users(basic_auth, grafana_url):
    #get users from ldaps
    #user = 'username:e.zhilenkov, group:UTZ'  #test datat 
    #print(f"Username:{user['username']}, Group:{user['group']}")
    id_user = user_contains("test@example.com") #ищем юзера в grafana 
    if(id_user!=None):
        res=get_teams(basic_auth,grafana_url) #получем все тимы 
        team_id=team_contains('Retail') #ищем тиму в grafana и получаем ее id 
        response =add_user_to_team(basic_auth,grafana_url,team_id,id_user)
        print(response)
    else:
        print("Функция sync_users не нашла пользователя")
    print(id_user)

def team_contains(basic_auth, grafana_url,search_string):
    teams=get_teams(basic_auth,grafana_url)
    search_name_lower = search_string.lower()
    for team in teams['teams']:
        if team['name'].lower() == search_name_lower:
            return team['id']
    return None

def user_contains(basic_auth, grafana_url,search_string):
    data=get_users(basic_auth,grafana_url)   
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        filtered_users = [user for user in data if search_string.lower() in user['name'].lower() or search_string.lower() in user['email'].lower()]

    for user in filtered_users:
        print(f"Name: {user['name']}, Id: {user['id']}, Email: {user['email']}, Last Seen: {user['lastSeenAt']}")
        return user['id']
    else:
        print("User not found in grafana")
 
def get_users(basic_auth, grafana_url):
    url = f"{grafana_url}/api/users"
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def create_team(basic_auth, grafana_url,team_name):
    url = f"{grafana_url}/api/teams"
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/json"
    }
    data = {
        "name": f"{team_name}", 
        "orgId": 1
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"Team {team_name} create successful. Id team: {response.json()['teamId']}")
    else:
        print(f"Failed to create team: {response.status_code}, {response.text}")
    return response.json()

def get_team_users(basic_auth, grafana_url,team_id):
    url = f"{grafana_url}/api/teams/{team_id}/members"
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

#https://grafana.com/docs/grafana/latest/developers/http_api/team/#remove-member-from-team
def remove_user_from_team(basic_auth, grafana_url,teamId,userId):
    url = f"{grafana_url}/api/teams/{teamId}/members/{userId}"
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code in [200, 201]:
        print(f"User {userId} remove from team {teamId} successful")
    else:
        print(f"Failed add user to team: {response.status_code}, {response.text}")
    return response.json()

#https://grafana.com/docs/grafana/latest/developers/http_api/team/#delete-team-by-id

def remove_team(basic_auth, grafana_url,teamId):
    url = f"{grafana_url}/api/teams/{teamId}"
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code in [200, 201]:
        print(f"Team {teamId} deleted")
    else:
        print(f"Failed add user to team: {response.status_code}, {response.text}")
    return response.json()
 