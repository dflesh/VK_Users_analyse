import sqlite3
from datetime import datetime, date, time


def create_db():
    year_now = str(datetime.now().year)
    month_now = str(datetime.now().month)
    day_now = str(datetime.now().day)
    date_now = year_now + '_' + month_now + '_' + day_now

    db_name = str(date_now) + '.db'

    connection = sqlite3.connect(db_name)
    return connection


def create_tables():
    connection = create_db()
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

    # cursor.execute('INSERT INTO vyatsu_group VALUES("yellow", "black")')
    # cursor.execute('SELECT * FROM VSU_Group')

    #print(cursor.fetchall())


def members_insert(members):
    connection = create_db()
    cursor = connection.cursor()
    print(*members, sep="\n")
    for i in members:
        for j in i:
            id = j['id']
            name = j['first_name'] + j['last_name']
            gender = ''
            if j['sex'] == 1:
                gender = 'Жен.'
            else:
                gender = 'Муж.'

            # TODO age calculating. Exception if birth date in member is not full {year-month-day}
            age = 0

            cursor.execute('INSERT INTO VSU_Member(id, name, gender, age) VALUES(?, ?, ?, ?)', [id, name, gender, age])

    connection.commit()
    connection.close()


def select_data():
    print('to do select data here')

