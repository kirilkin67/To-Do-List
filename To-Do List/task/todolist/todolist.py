# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.id}. {self.task} data:{self.deadline}"


MENU = """
1) Today's tasks
2) Add task
0) Exit"""


def menu_task():
    print(MENU)
    choice = input()
    if choice == "0":
        print("\nBye!")
    if choice == "1":
        today_task()
        menu_task()
    if choice == "2":
        add_task_database(input("Enter task\n> "))
        menu_task()


def add_task_database(new_task):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_row = Table(task=new_task)
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def today_task():
    Session = sessionmaker(bind=engine)
    session = Session()
    n = 0
    rows = session.query(Table).all()
    for row in rows:
        print(f"{n}. {row.task}")
        # if row.deadline == datetime.today():
        #     print(datetime.today())
        n += 1
        #     print(f"{n}. {row.task}")
    if n == 0:
        print("Nothing to do!")


def create_database():
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base = declarative_base()

    class Table(Base):
        __tablename__ = 'task'
        id = Column(Integer, primary_key=True)
        task = Column(String, default='default_value')
        deadline = Column(Date, default=datetime.today())

        def __repr__(self):
            return self.task

    Base.metadata.create_all(engine)


def main():
    create_database()
    menu_task()


main()


# create_database()
