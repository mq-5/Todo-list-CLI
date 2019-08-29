import os
import sys
import fire
import code
import sqlite3
from datetime import datetime
from termcolor import colored

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)
sql = """
  CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT "incomplete"
  )
"""

# sql = """
#     ALTER TABLE todos
#     ADD user_id INTEGER
# """
cur = conn.cursor()


def show_help_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored('Todo List Options:', 'blue'))
    print(colored('*' * 50, 'blue'))
    print(colored('1. List all todos:', 'blue'))
    print(colored('\t python3 todos.py list', 'white'))
    print(colored('2. Add a new todo:', 'blue'))
    print(colored('\t python3 todos.py add "My Todo Body"', 'white'))
    print(colored('3. Delete a todo:', 'blue'))
    print(colored('\t python3 todos.py delete 1', 'white'))
    print(colored('4. Mark a todo complete:', 'blue'))
    print(colored('\t python3 todos.py do 1', 'white'))
    print(colored('5. Mark a todo uncomplete:', 'blue'))
    print(colored('\t python3 todos.py undo 1', 'white'))
    print(colored('-' * 100, 'green'))

# TODOS


def add(body, project_id=None, user_id=None, due=datetime.now().date()):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored("Adding todo: ", "yellow"), body)
    sql = """
        INSERT INTO todos
        (body, due_date, project_id, user_id) VALUES (?, ?, ?, ?)
        """
    cur.execute(sql, (body, due, project_id, user_id))
    conn.commit()


def delete(id):
    os.system('cls' if os.name == 'nt' else 'clear')
    sql = """
        DELETE FROM todos
        WHERE id = ?
    """
    cur.execute(sql, (id,))
    conn.commit()
    print("Deleted row", id)


def show_list(key=None, value=None, status=None, col="due_date", order="ASC"):
    os.system('cls' if os.name == 'nt' else 'clear')

    if key and value and status:
        sql = f"""
        SELECT * FROM todos
        WHERE ? = ? 
        AND status = ? 
        ORDER BY {col} {order}   
        """
        cur.execute(sql, (key, value, status))
    elif key and value:
        sql = f"""
        SELECT * FROM todos
        WHERE {key} = ? 
        ORDER BY {col} {order}   
        """
        cur.execute(sql, (value,))
    else:
        sql = f"""
            SELECT * FROM todos
            ORDER BY {col} {order}    
        """
        cur.execute(sql)

    results = cur.fetchall()
    print(colored("Todos List:", "green"),
          colored('*' * 50, 'green'), sep="\n")
    for row in results:
        print(
            f'{colored("{}.".format(row[0]), "red")} {row[1]} | {row[2]} | {row[3]}')


def do(id):
    os.system('cls' if os.name == 'nt' else 'clear')
    sql = """
        UPDATE todos
        SET status = "complete"
        WHERE id = ?
    """
    cur.execute(sql, (id,))
    conn.commit()
    print('Task {} is done'.format(id))


def undo(id):
    os.system('cls' if os.name == 'nt' else 'clear')
    sql = """
        UPDATE todos
        SET status = "incomplete"
        WHERE id = ?
    """
    cur.execute(sql, (id,))
    conn.commit()
    print('Task {} is undone'.format(id))


def update_project(todo, project):
    sql = """
        UPDATE todos
        SET project_id = ?
        WHERE id = ?
    """
    cur.execute(sql, (project, todo))
    conn.commit()
    print("Project {1} is set to todo {0}".format(todo, project))


def update_user(todo, user):
    sql = """
        UPDATE todos
        SET user_id = ?
        WHERE id = ?
    """
    cur.execute(sql, (user, todo))
    conn.commit()
    print("User {} is set for todo {}".format(user, todo))

# USER


def add_user(name, email):
    sql = """
        INSERT INTO users
        (name, email) VALUES (?, ?)
    """
    cur.execute(sql, (name, email))
    conn.commit()


def list_users():
    sql = "SELECT * FROM users"
    cur.execute(sql)
    results = cur.fetchall()
    print('{:-^50}'.format("USER LIST"))
    for user in results:
        print(f'{user[0]}. {user[1]} | {user[2]}')


def staff():
    sql = """
        SELECT DISTINCT project_id, user_id, projects.name, users.name 
        FROM todos 
        JOIN projects ON todos.project_id = projects.id 
        JOIN users ON todos.user_id = users.id
    """
    cur.execute(sql)
    results = cur.fetchall()
    print('{:-^50}'.format("PROJECTS LIST"))
    for row in results:
        print(f'Project {row[2]} - {row[0]} | User {row[1]} {row[3]}')


def add_project(name):
    sql = """
        INSERT INTO projects
        (name) VALUES (?)    
    """
    cur.execute(sql, (name,))
    conn.commit()


def who_to_fire():
    pass


def list_projects():
    pass


if __name__ == '__main__':
    try:
        arg1 = sys.argv[1]
        if arg1 == '--help':
            show_help_menu()
        else:
            fire.Fire({
                'do': do,
                'add': add,
                'undo': undo,
                'delete': delete,
                'list': show_list,
                "staff": staff,
                'add_user': add_user,
                'list_users': list_users,
                "set_user": update_user,
                "add_project": add_project,
                "who_to_fire": who_to_fire,
                "set_project": update_project,
                "list_projects": list_projects
            })

    except IndexError:
        show_help_menu()
        sys.exit(1)
