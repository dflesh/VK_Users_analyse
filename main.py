import vk

session = vk.Session(access_token='d5b441ccd5b441ccd5b441cc0bd5d94752dd5b4d5b441cc883ce57ed215c145977b71cd')
api = vk.API(session)
v = 5.101

resp = api.groups.getMembers(group_id='vyatsu', v=v, offset='0')
print(len(resp['items']))
print(resp)