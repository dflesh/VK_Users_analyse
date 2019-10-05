import vk
import db

session = vk.Session(access_token='d5b441ccd5b441ccd5b441cc0bd5d94752dd5b4d5b441cc883ce57ed215c145977b71cd')
api = vk.API(session)
v = 5.101


def get_users():
    resp = api.groups.getMembers(group_id='prcom_vyatsu', v=v, offset='0')
    members = []
    offset = 0
    count = 1
    while offset < resp['count']:
        resp = api.groups.getMembers(group_id='prcom_vyatsu', v=v, offset=offset)
        offset += 1000
        for i in resp['items']:
            print(count)
            count += 1
            members.append(api.users.get(user_ids=i, v=v, fields='bdate, sex'))
            if count > 10:
                break
    return members


def get_communities(members):
    member_communities = []
    for i in members:
        for j in i:
            id = j['id']
            try:
                response = api.users.getSubscriptions(user_id=id, v=v, extended=1)
                print(response)
                subscriptions = response['items']
                all_groups = []
                for group in subscriptions:
                    print(group)
                    name = group['name']
                    print(name)
                    groupID = group['id']

                    all_groups.append({'id': groupID, 'name': name})
                member_communities.append({'id': id, 'subscriptions': all_groups})
            except:
                print('profile is private')
    print(*member_communities, sep='\n')

    return member_communities


def main():
    db.create_tables()
    members = get_users()
    member_communities = get_communities(members)
    db.members_insert(members)


main()
