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
    print(f"""
        {colored('{:-^100}'.format("TODOS OPTIONS"), 'blue')}
        {colored('1. List all todos:', 'blue')}
            python3 Todo.py list {colored('<column name> <column value> <status> <sort by> <ASD or DESC>', "yellow")}
        {colored('2. Add a new todo:', 'blue')}
            python3 Todo.py add {colored("<todo body> <project ID> <user ID> <due date>", "yellow")}
        {colored('3. Delete a todo:', 'blue')}
            python3 Todo.py delete {colored("<todo ID>", "yellow")}
        {colored('4. Mark a todo complete:', 'blue')}
            python3 Todo.py do {colored("<todo ID>", "yellow")}
        {colored('5. Mark a todo incomplete:', 'blue')}
            python3 Todo.py undo {colored("<todo ID>", "yellow")}
        {colored('6. Add new user:', 'blue')}
            python3 Todo.py add_user {colored("<user name> <user email>", "yellow")}
        {colored('7. List all users:', 'blue')}
            python3 Todo.py list_users
        {colored('8. List working staff:', 'blue')}
            python3 Todo.py staff
        {colored('9. Add new project:', 'blue')}
            python3 Todo.py add_project {colored("<project name>", "yellow")}
        {colored('10. List all projects:', 'blue')}
            python3 Todo.py list_projects
        {colored('11. Update project for current todo:', 'blue')}
            python3 Todo.py set_project {colored("<todo ID> <project ID>", "yellow")}
        {colored('12. Update user for current todo:', 'blue')}
            python3 Todo.py set_user {colored("<todo ID> <user ID>", "yellow")}
        {colored('13. Find out user not assigned to any todo:', 'blue')}
            python3 Todo.py who_to_fire
    """)

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
        status_color = "green" if row[3] == "incomplete" else "red"
        print(
            f'{colored("{}.".format(row[0]), "blue")} {row[1]} | {row[2]} | {colored(row[3], status_color)}')


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
    print('{:-^50}'.format("STAFF LIST"))
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
    os.system('cls' if os.name == 'nt' else 'clear')
    sql = """
        SELECT DISTINCT users.id, users.name, todos.project_id
        FROM users LEFT JOIN todos
        ON users.id = todos.user_id
        WHERE todos.project_id IS NULL
    """
    cur.execute(sql)
    results = cur.fetchall()
    print('{:-^50}'.format("FIRE LIST"))
    for row in results:
        print(f'{row[0]}. {colored(row[1], "blue")} has no task')


def list_projects():
    os.system('cls' if os.name == 'nt' else 'clear')
    sql = """
        SELECT * FROM projects
    """
    cur.execute(sql)
    results = cur.fetchall()
    print('{:-^50}'.format("PROJECTS LIST"))
    for row in results:
        print(f'{colored(row[0], "blue")}. {row[1]}')


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
