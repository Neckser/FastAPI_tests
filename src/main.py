from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3

app = FastAPI()


def verstka(spisok=[], n: int = None):
    h = """
    <html lang="ru">
    <head>
        <title>Задачи</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f3f4f6;
                margin: 0;
                padding: 20px;
            }
            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px;
                background-color: #ffffff;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            h1 {
                margin: 0;
            }
            form {
                display: flex;
                align-items: center;
                margin-bottom: 15px;
                background: #fff;
                padding: 15px;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .form-create {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-bottom: 20px;
            }
            .form-group {
                margin-bottom: 10px;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            input[type="text"], 
            input[type="number"],
            select,
            textarea {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                width: 100%;
                box-sizing: border-box;
            }
            textarea {
                min-height: 80px;
                resize: vertical;
            }
            button {
                padding: 10px 15px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #0056b3;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                padding: 15px;
                background-color: #e9ecef;
                margin: 5px 0;
                border-radius: 4px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .delete-button {
                background-color: #dc3545;
                border: none;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                cursor: pointer;
            }
            .delete-button:hover {
                background-color: #c82333;
            }
            .task-info {
                flex-grow: 1;
            }
            .task-actions {
                margin-left: 15px;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Задачи от Лично вас</h1>
            <form method="post" action="/find">
                <input type="text" name="string" placeholder="Поиск" required>
                <button type="submit">Найти</button>
            </form>
        </header>

        <form method="post" action="/create_task" class="form-create">
            <input type="hidden" name="name" value="{name}">
            <div class="form-group">
                <label for="task_name">Название задачи</label>
                <input type="text" id="task_name" name="task_name" required>
            </div>
            <div class="form-group">
                <label for="task_status">Статус</label>
                <select id="task_status" name="task_status" required>
                    <option value="">Выберите статус</option>
                    <option value="Активная">Активная</option>
                    <option value="В работе">В работе</option>
                    <option value="Завершена">Завершена</option>
                </select>
            </div>

            <div class="form-group">
                <label for="task_prioritet">Приоритет</label>
                <input type="number" id="task_prioritet" name="task_prioritet" min="1" max="10" required>
            </div>

            <div class="form-group">
                <label for="task_opis">Описание</label>
                <textarea id="task_opis" name="task_opis" required></textarea>
            </div>

            <div class="form-group" style="grid-column: span 2;">
                <button type="submit" style="width: 100%;">Создать задачу</button>
            </div>
        </form>

        <form method="post" action="/prioritet">
            <input type="number" name="number" placeholder="Топ самых приоритетных задач" min="1" required>
            <button type="submit">Показать</button>
        </form>

        <ul>
    """
    for i in range(n):
        h += f"""
        <li>
            <div class="task-info">
                <strong>id: {spisok[i][0]}</strong><br>
                <strong>Имя:</strong> {spisok[i][1]}<br>
                <strong>Статус:</strong> {spisok[i][2]}<br>
                <strong>Описание:</strong> {spisok[i][3]}<br>
                <strong>Приоритет:</strong> {spisok[i][4]}<br>
                <strong>Дата создания:</strong> {spisok[i][5]}
            </div>
            <div class="task-actions">
                <form method="post" action="/delete_task/{spisok[i][0]}" style="display:inline;">
                    <button type="submit" class="delete-button">Удалить</button>
                </form>
            </div>
        </li>
        """
    h += """
            </ul>
            <p>Отсортировать по:</p>
            <a href="/status"><button>Cтатусу</button></a>
            <a href="/data"><button>Дате</button></a>
            <a href="/name"><button>Имени</button></a>
            <a href="/priority"><button>Приоритету</button></a>
        </body>
        </html>
    """
    return h


@app.get("/")
def startlog():
    with open("src/login.html", "r", encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)


@app.post("/login")
def login(login: str = Form(...), password: str = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logins (
        login TEXT,
        password TEXT,
        name TEXT
    )''')
    connection.commit()
    cursor.execute("SELECT * FROM logins WHERE login = ? AND password = ?", (login, password))
    res = cursor.fetchall()
    connection.close()
    if res:
        return RedirectResponse(url=f"/well?name={login}", status_code=303)
    else:
        with open("src/wrongpassword.html", "r", encoding='utf-8') as file:
            content = file.read()
        return HTMLResponse(content=content)


@app.get("/register")
def get_registration():
    with open('src/registration.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)


@app.post("/register")
def registration(login: str = Form(...), password: str = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logins (
        login TEXT,
        password TEXT,
        name TEXT
    )''')
    connection.commit()
    cursor.execute("INSERT INTO logins (login, password, name) VALUES (?, ?, ?)", (login, password, login + password))
    connection.commit()
    connection.close()
    return RedirectResponse(url=f"/", status_code=303)


@app.get('/well')
def well(name: str = None):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS user_tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        task_status TEXT,
        task_opis TEXT,
        task_prioritet INTEGER,
        task_time DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute(f"SELECT * FROM user_tasks")
    colvo = cursor.fetchall()
    connection.close()
    if colvo:
        return HTMLResponse(content=verstka(colvo, len(colvo)))
    else:
        return HTMLResponse(content=verstka([], 0))


@app.post("/create_task")
def create_task(task_name: str = Form(...),task_status: str = Form(...),task_prioritet: int = Form(...),task_opis: str = Form(...),name: str = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            task_status TEXT,
            task_opis TEXT,
            task_prioritet INTEGER,
            task_time DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute('''INSERT INTO user_tasks (task_name, task_status, task_opis, task_prioritet) VALUES (?, ?, ?, ?)''',(task_name, task_status, task_opis, task_prioritet))
    connection.commit()
    connection.close()
    return RedirectResponse(url=f"/well?name={name}", status_code=303)

@app.post("/delete_task/{task_id}")
def delete_task(task_id: int):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        task_status TEXT,
        task_opis TEXT,
        task_prioritet INTEGER,
        task_time DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute(f"DELETE FROM user_tasks WHERE task_id = ?", (task_id,))
    connection.commit()
    connection.close()
    return RedirectResponse(url=f"/well", status_code=303)


@app.post("/find")
def find_tasks(string: str = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM user_tasks WHERE task_name LIKE ? OR task_opis LIKE ?''', (f'%{string}%', f'%{string}%'))
    tasks = cursor.fetchall()
    connection.close()
    return HTMLResponse(content=verstka(tasks, len(tasks)))

@app.get("/status")
def sort_by_status():
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM user_tasks ORDER BY task_status''')
    tasks = cursor.fetchall()
    connection.close()
    return HTMLResponse(content=verstka(tasks, len(tasks)))

@app.get("/data")
def sort_by_date():
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM user_tasks ORDER BY task_time''')
    tasks = cursor.fetchall()
    connection.close()
    return HTMLResponse(content=verstka(tasks, len(tasks)))


@app.get("/name")
def sort_by_name():
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM user_tasks ORDER BY task_name''')
    tasks = cursor.fetchall()
    connection.close()
    return HTMLResponse(content=verstka(tasks, len(tasks)))


@app.get("/priority")
def sort_by_priority():
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM user_tasks ORDER BY task_prioritet''')
    tasks = cursor.fetchall()
    connection.close()
    return HTMLResponse(content=verstka(tasks, len(tasks)))


@app.post("/prioritet")
def show_top_priority(number: int = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM user_tasks ORDER BY task_prioritet LIMIT ?''', (number,))
    tasks = cursor.fetchall()
    connection.close()
    return HTMLResponse(content=verstka(tasks, len(tasks)))
