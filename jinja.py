import sqlite3
from jinja2 import Environment, FunctionLoader, PackageLoader, PrefixLoader, DictLoader, FileSystemLoader

html = '''
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  </head>
  <body>
      Hello
      <br>
      {% for user in members %}
        <li>{{ user }}</li>
      {% endfor %}
      <br>
  </body>
</html>
'''


def create_conn(db_file):
    conn = None
    conn = sqlite3.connect(db_file)
    return conn


def select_mem(conn):
    rows = []
    cur = conn.cursor()
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age < 18")
    rows.append(cur.fetchall())
    print(type(cur.fetchall()))
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 18 and age < 21")
    rows.append(cur.fetchall())
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 21 and age < 24")
    rows.append(cur.fetchall())
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 24 and age < 27")
    rows.append(cur.fetchall())
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 27 and age < 30")
    rows.append(cur.fetchall())
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 30 and age < 35")
    rows.append(cur.fetchall())
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age >= 35 and age < 45")
    rows.append(cur.fetchall())
    cur.execute("SELECT count(name) FROM VSU_Member WHERE age > 45")
    # rows = cur.fetchall()
    rows.append(cur.fetchall())

    print(rows)
    return rows


env = Environment(loader = DictLoader({'index.html': html}))
template = env.get_template('index.html')
# print(template.render(name=members[0], photo_50 = member_communities[0]))
# conn = create_connection(r"D:\5th Semestr\MMAD\vkAnalyse\vk_members_2019_10_21.db")
with open("new.html", "w") as f:
    f.write(template.render(members = select_mem(create_conn(r"D:\\5th Semestr\\MMAD\\vkAnalyse\\vk_members_2019_10_22.db"))))
