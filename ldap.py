from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES, ALL, ALL_OPERATIONAL_ATTRIBUTES

def get_users(group,server_url, user, password, ou_dn):
    # Параметры подключения 
    group_dn = f'CN={group},{ou_dn}'
 
    try:
        # Создание объекта сервера
        server = Server(server_url, use_ssl=True)

        # Создание объекта подключения
        conn = Connection(server, user=user, password=password, auto_bind=True)

        # Поиск членов группы "Grafana - Retail"
        conn.search(group_dn, '(objectClass=*)', search_scope=SUBTREE, attributes=['member'])

        # Инициализация списка для хранения результатов
        result = []

        # Обработка каждого члена группы
        for entry in conn.entries:
            members = entry['member'].values if 'member' in entry else []
            for member_dn in members:
                # Получаем информацию о пользователе по его DN
                conn.search(member_dn, '(objectClass=user)', search_scope=SUBTREE, attributes=['sAMAccountName', 'mail'])
                user_entry = conn.entries[0] if conn.entries else None
                
                if user_entry:
                    username = user_entry['sAMAccountName'].value if 'sAMAccountName' in user_entry else ''
                    email = user_entry['mail'].value if 'mail' in user_entry else ''
                    
                    result.append({
                        'group': group,
                        'username': username,
                        'email': email
                    })

        # Закрытие соединения
        conn.unbind()

        return result

    except Exception as e:
        print(f"Error: {e}")
        return []
  
def get_groupname(server_url, user, password, ou_dn): 
    # Параметры подключения    
    # Создание объекта сервера
    server = Server(server_url, use_ssl=True)
    
    # Создание объекта подключения
    conn = Connection(server, user, password, auto_bind=True)
    
    # Поиск всех групп в указанной организационной единице
    conn.search(ou_dn, '(objectClass=group)', search_scope=SUBTREE, attributes=['cn'])
    
    # Вывод результатов поиска
    for entry in conn.entries:
        group_name = entry.cn.value
        print(group_name)
    
    # Закрытие соединения
    conn.unbind()
    return conn.entries
 

##users = get_users('Grafana - Retail',password)
#users = get_users('Grafana - Retail',password)
#print(users)
## Пример поиска пользователя по имени
#username_to_find = 'e.zhilenkov'
#found_users = [user for user in users if user['username'] == username_to_find]
#
#for user in found_users:
#    print(f"Group: {user['group']}, Username: {user['username']}, Email: {user['email']}")

