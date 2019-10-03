import vk
import db

session = vk.Session(access_token='d5b441ccd5b441ccd5b441cc0bd5d94752dd5b4d5b441cc883ce57ed215c145977b71cd')
api = vk.API(session)
v = 5.101


def get_users():
    resp = api.groups.getMembers(group_id='prcom_vyatsu', v=v, offset='0')
    members = []
    # print(resp['items'])
    offset = 0
    count = 1
    while offset < 1001:
        resp = api.groups.getMembers(group_id='prcom_vyatsu', v=v, offset=offset)
        offset += 1000
        for i in resp['items']:
            # print(count)
            count += 1
            members.append(api.users.get(user_ids=i, v=v, fields='bdate, sex'))

            if count > 5:
                break

    db.create_tables()
    db.members_insert(members)
    # print(*members, sep="\n")


def main():
    get_users()


main()
