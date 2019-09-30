import sqlite3

connection = sqlite3.connect('VkUserAnalyse.sqlite')

#открываем соединение
cursor = connection.cursor()

#cоздание таблицы группы вятгу
cursor.execute(""""Create table Group
                    """)

#таблица пользователей
cursor.execute("""Crate table User
               """)

#таблица групп пользователей


#таблица возрастов


#таблица лайков


#таблица репостов


#таблица комментариев





#закрываем соединение
connection.close()