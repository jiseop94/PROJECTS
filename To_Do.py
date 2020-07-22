from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

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


def show_task():
    rows = session.query(Table).all()
    if len(rows) == 0:
        print("Today:")
        print("Nothing to do!\n")
    else:
        print("Today:")
        for i in range(len(rows)):
            print((i + 1), '.', rows[i].task)
        print('')


def add_task():
    print("Enter task")

    new_task = input()
    new_row = Table(task=new_task.lstrip())

    session.add(new_row)
    session.commit()

    print("The task has been added!\n")


flag = True

while flag:

    print("1) Today's tasks")
    print("2) Add task")
    print("0) Exit")
    menu = input()
    print('')

    if menu.lstrip("> ") == '1':
        show_task()
    elif menu.lstrip("> ") == '2':
        add_task()
    elif menu.lstrip("> ") == '0':
        print("Bye!")
        flag = False
