import vk
import db
import time

session = vk.Session(access_token='d5b441ccd5b441ccd5b441cc0bd5d94752dd5b4d5b441cc883ce57ed215c145977b71cd')
api = vk.API(session)
v = 5.101


def get_users():
    response = api.groups.getMembers(group_id='prcom_vyatsu', v=v, offset='0')
    members = []
    offset = 0
    count = 1
    while offset < response['count']:
        response = api.groups.getMembers(group_id='prcom_vyatsu', v=v, offset=offset)
        offset += 1000
        for member_id in response['items']:
            count += 1
            members.append(api.users.get(user_ids=member_id, v=v, fields='bdate, sex'))
            # if count > 10:
            #     break
    return members


def get_communities(members):
    member_communities = []
    for member in members:
        # print(member)
        for info in member:
            member_id = info['id']
            try:
                response = api.users.getSubscriptions(user_id=member_id, v=v, extended=1)
                subscriptions = response['items']
                all_communities = []
                for community in subscriptions:
                    community_name = community['name']
                    community_id = community['id']

                    all_communities.append({'id': community_id, 'name': community_name})
                member_communities.append({'id': member_id, 'subscriptions': all_communities})
            except:
                print('profile is private')
    return member_communities


def get_vsu_group():
    vsu_group = api.groups.getById(group_id='prcom_vyatsu', v=v, fields='description')
    return vsu_group


def get_vsu_posts():
    counter = 0
    offset = 0
    response = api.wall.get(owner_id='-108366262', v=v, offset=offset, filter='owner')
    count = response['count']
    # print(count)
    posts = {}
    while offset < count:
        response = api.wall.get(owner_id='-108366262', v=v, count=count, offset=offset, filter='owner')
        offset += 100
        for post in response['items']:
            # print(post)
            posts[counter] = post['id']
            counter += 1
            if counter > count:
                break
    return posts


def get_activity(posts, users_ids):
    activity = []
    for i in posts:
        post_id = posts[i]
        # print(post_id)
        likes_list = api.likes.getList(type='post', item_id=post_id, v=v, filter='likes', owner_id='-108366262')
        comments_list = api.wall.getComments(owner_id='-108366262', post_id=post_id, v=v)
        # print(comments_list)
        # print(likes_list)
        if likes_list['count'] != 0:
            for like in likes_list['items']:
                for comment in comments_list['items']:
                    # print(comment)
                    for user_id in users_ids:
                        if user_id == like:
                            like_flag = 1
                        else:
                            like_flag = 0
                        if user_id == comment['from_id']:
                            comment_flag = 1
                        else:
                            comment_flag = 0
                        if like_flag == 1 or comment_flag == 1:
                            activity.append({'userID': user_id, 'postID': post_id,
                                             'like': like_flag, 'comment': comment_flag})
    # print(*activity, sep='\n')
    return activity


def main():
    db.create_tables()
    members = get_users()
    db.members_insert(members)
    member_communities = get_communities(members)
    db.member_community_insert(member_communities)
    vsu_group = get_vsu_group()
    db.vsu_community_insert(vsu_group)
    users = db.select_users_ids()
    posts = get_vsu_posts()
    activities = get_activity(posts, users)
    db.insert_activities(activities)


start_time = time.time()
print(start_time)
main()
print(time.time() - start_time)
