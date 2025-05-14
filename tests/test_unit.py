import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import verstka

tasks = [(1, "Test Task", "Активная", "Описание задачи", 5, "2024-01-01 12:00:00"),
         (2, "Закончить отчёт", "Активная", "Важно", 1, "2024-01-02 13:00:00"),
         (3, "Позвонить", "В работе", "Нужно срочно", 2, "2024-01-03 14:00:00"),
         (4, "Сделать Матанализ", "Закончен", "БДЗ4", 1, "2024-01-04 15:00:00"),
         (5, "ИПР тестирование", "В работе", "2 дз", 1, "2024-01-05 16:00:00"), ]


def test_verstka_empty():
    html = verstka([], 0)
    assert html.count("<ul>") > 0 and html.count("</ul>") > 0
    assert html.count("<li>") == 0 and html.count("</li>") == 0
    assert html.count("Задачи от Лично вас") > 0

def test_verstka_one():
    html = verstka(tasks, len(tasks))
    for i in range(len(tasks)):
        assert html.count(str(tasks[i][0])) > 0
        assert html.count(str(tasks[i][1])) > 0
        assert html.count(str(tasks[i][2])) > 0
        assert html.count(str(tasks[i][3])) > 0
        assert html.count(str(tasks[i][4])) > 0
        assert html.count(str(tasks[i][5])) > 0

def test_verstka_links():
    html = verstka(tasks, len(tasks))
    assert html.count('href="/status"') > 0
    assert html.count('href="/data"') > 0
    assert html.count('href="/name"') > 0
    assert html.count('href="/priority"') > 0
    assert html.count('form method="post" action="/find"') > 0
    assert html.count('form method="post" action="/create_task"') > 0

def test_verstka_delbutton():
    html = verstka(tasks, len(tasks))
    for task in tasks:
        assert html.count(f'action="/delete_task/{task[0]}"') > 0
        assert html.count('class="delete-button"') > 0
