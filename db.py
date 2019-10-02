import sqlite3
from datetime import datetime, date, time


def create_db():
    year_now = str(datetime.now().year)
    month_now = str(datetime.now().month)
    day_now = str(datetime.now().day)
    date_now = year_now + '_' + month_now + '_' + day_now

    db_name = str(date_now) + '.db'
    print(db_name)
    connection = sqlite3.connect(db_name)
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
                   'age integer, '
                   'href text)')

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


    # cursor.execute('INSERT INTO vyatsu_group VALUES("yellow", "black")')
    # cursor.execute('SELECT * FROM VSU_Group')

    #print(cursor.fetchall())

    connection.commit()
    connection.close()


def main():
    create_db()

