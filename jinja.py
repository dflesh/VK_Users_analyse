# -*- coding: utf-8 -*-
import sqlite3
import pandas as pand
import matplotlib.pyplot as plt
from jinja2 import Environment, FunctionLoader, PackageLoader, PrefixLoader, DictLoader, FileSystemLoader


def create_conn(db_file):
    conn = None
    conn = sqlite3.connect(db_file)
    return conn


def select_mem(conn):
    rows = []
    cur = conn.cursor()
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age < 18")
    rows.append(cur.fetchall()[0])
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 18 and age < 21")
    rows.append(cur.fetchall()[0])
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 21 and age < 24")
    rows.append(cur.fetchall()[0])
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 24 and age < 27")
    rows.append(cur.fetchall()[0])
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 27 and age < 30")
    rows.append(cur.fetchall()[0])
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 30 and age < 35")
    rows.append(cur.fetchall()[0])
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 35 and age < 45")
    rows.append(cur.fetchall()[0])
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age > 45")
    rows.append(cur.fetchall()[0])
    rows = list(sum(rows, ()))
    summa = sum(rows)
    x_row = ["< 18","18-21","21-24","24-27","27-30","30-35","35-45","> 45"]
    for i in range(rows.__len__()):
        rows[i] = rows[i] * 100 / summa
    dataframe = pand.DataFrame()
    dataframe['Проценты'] = rows
    dataframe['Категории'] = x_row
    agraph = dataframe.plot(x = 'Категории', kind = 'bar', color = 'teal')
    agraph.set(xlabel = "Категории возрастов", ylabel = "Проценты")
    plt.tight_layout()
    plt.savefig('templates/screenshots/categoryGroups.png')
    return rows


def top_communityM(conn, gen):
    cur = conn.cursor()
    cur.execute("select VSU_Member_Community.name, count(*) from VSU_Member_Community join VSU_Member on VSU_Member_Community.memberID = VSU_Member.id where VSU_Member.gender =:gen group by VSU_Member_Community.name order by count(*) DESC limit 5", {"gen": gen})
    data = cur.fetchall()
    name =  []
    count = []
    for row in data:
        name.append(row[0])
        count.append(row[1])
    dataframe = pand.DataFrame()
    dataframe["Имена"] = name
    dataframe["Количество"] = count
    cgraph = dataframe.plot(x = 'Имена', kind = 'bar', color = 'c')
    cgraph.set(xlabel = "Названия групп", ylabel = "Количество")
    plt.tight_layout()
    if gen == 'Муж.':
        plt.savefig('templates/screenshots/mensTOP5.png')
    else:
        plt.savefig('templates/screenshots/womensTOP5.png')


def top_ages(conn, gen):
    data = []
    cur = conn.cursor()
    cur.execute("select VSU_Member_Community.name, count(*) from VSU_Member_Community join VSU_Member on VSU_Member_Community.memberID = VSU_Member.id where VSU_Member.gender =:gen and VSU_Member.age < 18 group by VSU_Member_Community.name order by count(*) DESC limit 5", {"gen": gen})
    data.append(cur.fetchall())
    cur.execute("select VSU_Member_Community.name, count(*) from VSU_Member_Community join VSU_Member on VSU_Member_Community.memberID = VSU_Member.id where VSU_Member.gender =:gen and VSU_Member.age >= 18 and VSU_Member.age < 21 group by VSU_Member_Community.name order by count(*) DESC limit 5", {"gen": gen})
    data.append(cur.fetchall())
    cur.execute("select VSU_Member_Community.name, count(*) from VSU_Member_Community join VSU_Member on VSU_Member_Community.memberID = VSU_Member.id where VSU_Member.gender =:gen and VSU_Member.age >= 21 and VSU_Member.age < 24 group by VSU_Member_Community.name order by count(*) DESC limit 5", {"gen": gen})
    data.append(cur.fetchall())
    cur.execute("select VSU_Member_Community.name, count(*) from VSU_Member_Community join VSU_Member on VSU_Member_Community.memberID = VSU_Member.id where VSU_Member.gender =:gen and VSU_Member.age >= 24 and VSU_Member.age < 27 group by VSU_Member_Community.name order by count(*) DESC limit 5", {"gen": gen})
    data.append(cur.fetchall())
    cur.execute("select VSU_Member_Community.name, count(*) from VSU_Member_Community join VSU_Member on VSU_Member_Community.memberID = VSU_Member.id where VSU_Member.gender =:gen and VSU_Member.age >= 27 and VSU_Member.age < 30 group by VSU_Member_Community.name order by count(*) DESC limit 5", {"gen": gen})
    data.append(cur.fetchall())
    cur.execute("select VSU_Member_Community.name, count(*) from VSU_Member_Community join VSU_Member on VSU_Member_Community.memberID = VSU_Member.id where VSU_Member.gender =:gen and VSU_Member.age >= 30 and VSU_Member.age < 35 group by VSU_Member_Community.name order by count(*) DESC limit 5", {"gen": gen})
    data.append(cur.fetchall())
    cur.execute("select VSU_Member_Community.name, count(*) from VSU_Member_Community join VSU_Member on VSU_Member_Community.memberID = VSU_Member.id where VSU_Member.gender =:gen and VSU_Member.age >= 35 and VSU_Member.age < 45 group by VSU_Member_Community.name order by count(*) DESC limit 5", {"gen": gen})
    data.append(cur.fetchall())
    cur.execute("select VSU_Member_Community.name, count(*) from VSU_Member_Community join VSU_Member on VSU_Member_Community.memberID = VSU_Member.id where VSU_Member.gender =:gen and VSU_Member.age >= 45 group by VSU_Member_Community.name order by count(*) DESC limit 5", {"gen": gen})
    data.append(cur.fetchall())
    x_row = ["меньше 18", "от 18 до 21", "от 21 до 24", "от 24 до 27", "от 27 до 30", "от 30 до 35", "от 35 до 45", "больше 45"]
    graphs = []
    for i in range(data.__len__()):
        name = []
        count = []
        for row in data[i]:
            name.append(row[0])
            count.append(row[1])
        dataframe = pand.DataFrame()
        dataframe["Имена"] = name
        dataframe["Количество"] = count
        if gen == 'Жен.':
            cgraph = dataframe.plot(x='Имена', kind='bar', color='c', title  = "Женщины " + x_row[i])
            cgraph.set(xlabel="Названия групп", ylabel="Количество")
            plt.tight_layout()
            plt.savefig('templates/screenshots/top5_W'+str(i)+'.png')
            graphs.append('screenshots/top5_W'+str(i)+'.png')
        else:
            cgraph = dataframe.plot(x='Имена', kind='bar', color='c', title="Мужчины " + x_row[i])
            cgraph.set(xlabel="Названия групп", ylabel="Количество")
            plt.tight_layout()
            plt.savefig('templates/screenshots/top5_M' + str(i) + '.png')
            graphs.append('screenshots/top5_M' + str(i) + '.png')
    return graphs


env = Environment(loader = FileSystemLoader('templates/'))
template = env.get_template('templateRE.html')

select_mem(create_conn(r"D:\\5th Semestr\\MMAD\\vkAnalyse\\vk_members_2019_10_22.db"))
top_communityM(create_conn(r"D:\\5th Semestr\\MMAD\\vkAnalyse\\vk_members_2019_10_22.db"), 'Жен.')
top_communityM(create_conn(r"D:\\5th Semestr\\MMAD\\vkAnalyse\\vk_members_2019_10_22.db"), 'Муж.')
graphs = top_ages(create_conn(r"D:\\5th Semestr\\MMAD\\vkAnalyse\\vk_members_2019_10_22.db"), 'Жен.')
tgraphs = top_ages(create_conn(r"D:\\5th Semestr\\MMAD\\vkAnalyse\\vk_members_2019_10_22.db"), 'Муж.')

with open("templates/new.html", "w") as f:
    f.write(template.render(url1 = 'screenshots/categoryGroups.png', url2 = 'screenshots/womensTOP5.png', url3 = 'screenshots/mensTOP5.png', mems = graphs))

