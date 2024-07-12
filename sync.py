import schedule
import time
from datetime import datetime
import grafana
import ldap
import json


# Open and read the JSON file
with open('conf.json', 'r') as file:
    data = json.load(file)


basic_auth = data['grafana']['basic_auth']
grafana_url = data['grafana']['grafana_url']  
auto_create_teams = data['grafana']['auto_create_teams']  
##Роли с который функции user_to_org и user_to_team распихивают юзеров в графане##
team_role = data['roles']['to_team']
org_role = data['roles']['to_org']
####################################################################################
ldap_user = data['ldap']['user']
ldap_password = data['ldap']['password']
ldap_server_url = data['ldap']['server_url']
ldap_ou_dn = data['ldap']['ou_dn']

 
#print(f"Basic Auth: {basic_auth}")
#print(f"Grafana URL: {grafana_url}")
#print(f"Org Role: {org_role}")
#print(f"Team Role: {team_role}")




def sync ():
    print(f"function sync start {datetime.now().time()}")
    groups = ldap.get_groupname(ldap_server_url, ldap_user, ldap_password, ldap_ou_dn)
    for group in groups: 
        #получаем id team в grafana (название группы AD = team grafana)
        id_team=grafana.team_contains(basic_auth,grafana_url, group.cn.value)

        #если в конфиге "auto_create_teams": true и группы не существует то создаем ёё
        if(auto_create_teams==True and id_team==None):  
            id_team=grafana.create_team(basic_auth,grafana_url,group.cn.value)['teamId']

        if(id_team!=None):
            ldap_users = ldap.get_users(group.cn.value,ldap_server_url, ldap_user, ldap_password, ldap_ou_dn)  
            ldap_usernames = {user['username'] for user in ldap_users}
            grafana_users = grafana.get_team_users(basic_auth,grafana_url,id_team)
            grafana_usernames = {user['login'] for user in grafana_users}

            missing_users = ldap_usernames - grafana_usernames
            remove_users = grafana_usernames - ldap_usernames
            ### сравнить два массива###

            for user in missing_users:
                user_id = grafana.user_contains(basic_auth,grafana_url,user)
                grafana.add_user_to_team(basic_auth,grafana_url,id_team,user_id) 

            for user in remove_users:
                user_id = grafana.user_contains(basic_auth,grafana_url,user)
                grafana.remove_user_from_team(basic_auth,grafana_url,id_team,user_id)


#schedule.every(1).minutes.do(sync)

while True:
    #schedule.run_pending()
    sync()
    time.sleep(60)