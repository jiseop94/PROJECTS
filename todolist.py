# Write your code here
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

# from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


def show_today_task():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()

    # print(today.date())

    if len(rows) == 0:
        print("Today", today.day, today.strftime('%b') + ":")
        print("Nothing to do!\n")
    else:
        print("Today", today.day, today.strftime('%b') + ":")
        for i in range(len(rows)):
            print(str(i + 1) + '.', rows[i].task)

        print('')


def add_task():
    print("Enter task")
    new_task = input()

    print("Enter deadline")
    str_date = input()
    d_date = datetime.strptime(str_date.lstrip('>'), "%Y-%m-%d")

    new_row = Table(task=new_task.lstrip('>'),
                    deadline=d_date)

    session.add(new_row)
    session.commit()

    print("The task has been added!\n")


def show_week_task():
    weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    today = datetime.today()

    for j in range(7):
        rows = session.query(Table).filter(Table.deadline ==
                                           (today + timedelta(days=j)).date()).all()
        if len(rows) == 0:
            print(weekDays[(today + timedelta(days=j)).weekday()],
                  (today + timedelta(days=j)).day,
                  (today + timedelta(days=j)).strftime('%b') + ':')
            print("Nothing to do!\n")
        else:
            # print(rows[j].day, rows[j].strftime('%b'))
            print(weekDays[(today + timedelta(days=j)).weekday()],
                  (today + timedelta(days=j)).day,
                  (today + timedelta(days=j)).strftime('%b') + ':')
            for i in range(len(rows)):
                # if rows[i].deadline == today.date():
                print((i + 1), '.', rows[i].task)
            print("")


def show_all_task():
    print("All tasks:")
    rows = session.query(Table).all()
    sorted_rows = sorted(rows, key=lambda x: x.deadline)
    # print(type(rows))
    for i in range(len(sorted_rows)):
        print(str(i + 1) + '.', sorted_rows[i].task + '.',
              sorted_rows[i].deadline.day,
              sorted_rows[i].deadline.strftime('%b'))
    print("")


def show_missed_task():
    print("Missed tasks:")
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline < today.date()).all()
    sorted_rows = sorted(rows, key=lambda x: x.deadline)
    for i in range(len(sorted_rows)):
        print(str(i + 1) + '.', sorted_rows[i].task + '.',
              sorted_rows[i].deadline.day,
              sorted_rows[i].deadline.strftime('%b'))
    print("")


def delete_task():
    print("Chose the number of the task you want to delete:")

    rows = session.query(Table).order_by(Table.deadline).all()
    for i in range(len(rows)):
        print(str(i + 1) + '.', rows[i].task + '.',
              rows[i].deadline.day,
              rows[i].deadline.strftime('%b'))
    num = int(input(">"))
    if num == 0:
        print("Nothing deleted!\n")
    else:
        session.delete(rows[num - 1])
        print("The task has been deleted!\n")
        session.commit()


"""
    rows = session.query(Table).all()
    sorted_rows = sorted(rows, key=lambda x: x.deadline)
    # print(type(rows))
    for i in range(len(sorted_rows)):
        print(str(i + 1) + '.', sorted_rows[i].task + '.',
              sorted_rows[i].deadline.day,
              sorted_rows[i].deadline.strftime('%b'))
    print("")

    num = int(input(">"))
    if num == 0:
        print("Nothing deleted!\n")
    else:
        session.delete(sorted_rows[num - 1])
        print("The task has been deleted!\n")
        session.commit()
"""

flag = True

while flag:

    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    menu = input()
    print('')

    if menu.lstrip("> ") == '1':
        show_today_task()
    elif menu.lstrip("> ") == '2':
        show_week_task()
    elif menu.lstrip("> ") == '3':
        show_all_task()
    elif menu.lstrip("> ") == '4':
        show_missed_task()
    elif menu.lstrip("> ") == '5':
        add_task()
    elif menu.lstrip("> ") == '6':
        delete_task()
    elif menu.lstrip("> ") == '0':
        print("Bye!")
        flag = False
