import sqlite3
from datetime import datetime
import re
import os


def create_db(remove):
    year_now = str(datetime.now().year)
    month_now = str(datetime.now().month)
    day_now = str(datetime.now().day)

    date_now = year_now + '_' + month_now + '_' + day_now

    db_name = 'vk_members_' + str(date_now) + '.db'

    if os.path.isfile(db_name) and remove:
        os.remove(db_name)

    connection = sqlite3.connect(db_name)
    return connection


def create_tables():
    connection = create_db(True)
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE VSU_Community'
                   '(id integer primary key, '
                   'name text, '
                   'info text, '
                   'href text)')

    cursor.execute('CREATE TABLE VSU_Member'
                   '(id integer primary key, '
                   'name varchar(100), '
                   'gender varchar(10), '
                   'age integer)')

    cursor.execute('CREATE TABLE VSU_Member_Activity'
                   '(like integer,'
                   'repost integer,'
                   'comment integer,'
                   'postID integer,'
                   'memberID integer,'
                   'communityID integer, '
                   'foreign key(memberID) references VSU_Member(id),'
                   'foreign key(communityID) references VSU_Community(id))')

    cursor.execute('CREATE TABLE VSU_Member_Community'
                   '(memberID integer,'
                   'communityID integer, '
                   'href text, '
                   'name text,'
                   'foreign key(memberID) references VSU_Member(id))')

    connection.commit()
    connection.close()


def members_insert(members):
    connection = create_db(False)
    cursor = connection.cursor()

    for i in members:
        for j in i:
            id = j['id']
            name = j['first_name'] + ' ' + j['last_name']
            gender = ''
            if j['sex'] == 1:
                gender = 'Жен.'
            else:
                gender = 'Муж.'

            # Do Age calculating
            bdate = ''
            # Check bdate for exist in dictionary
            if 'bdate' in j:
                # Check bdate for completeness ( dd-mm-yy )
                bdate = re.match('([0-9]+?.[0-9]+?.[0-9]+)', j['bdate'])
            age = None
            if bdate:
                birth_date = bdate.group(0).split('.')
                day_bdate = int(birth_date[0])
                month_bdate = int(birth_date[1])
                year_bdate = int(birth_date[2])
                year_now = int(datetime.now().year)
                month_now = int(datetime.now().month)
                day_now = int(datetime.now().day)
                # Age calculating
                if day_now < day_bdate and month_now < month_bdate:
                    age = str(year_now - year_bdate)
                else:
                    age = str(year_now - year_bdate - 1)
            elif bdate is None:
                age = None

            cursor.execute('INSERT INTO VSU_Member(id, name, gender, age) VALUES(?, ?, ?, ?)', [id, name, gender, age])

    connection.commit()
    connection.close()
