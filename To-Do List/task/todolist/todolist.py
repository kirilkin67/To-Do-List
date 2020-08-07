# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

MENU = """
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit"""

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.id}. {self.task} data:{self.deadline}"


class MyToDo:
    def __init__(self, file_name):
        self.engine = create_engine(f'sqlite:///{file_name}.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.menu_tasks()

    def menu_tasks(self):
        while True:
            print(MENU)
            today = datetime.today()
            choice = input("> ")
            if choice == "0":
                print("\nBye!")
                break
            if choice == "1":
                self.today_tasks(today)
            if choice == "2":
                self.week_tasks(today)
            if choice == "3":
                self.all_tasks(today)
            if choice == "4":
                self.missed_tasks(today)
            if choice == "5":
                self.add_task_database()
            if choice == "6":
                self.delete_task()

    def add_task_database(self):
        new_task = input("\nEnter task\n>")
        deadline = input("Enter deadline\n>")
        try:
            if deadline:
                new_row = Table(task=new_task,
                                deadline=datetime.strptime(deadline, '%Y-%m-%d').date())
            else:
                new_row = Table(task=new_task)
            self.session.add(new_row)
            self.session.commit()
        except ValueError:
            print("Please, Enter Deadline, Format Example: '%Y-%m-%d' - '2020-04-24'")
        else:
            print("The task has been added!")

    def today_tasks(self, today):
        title = f"Today {today.day} {today.strftime('%b')}"
        rows = self.session.query(Table).filter(Table.deadline == today.date()).all()
        self.tasks_print(title, rows, form=False)

    def week_tasks(self, today):
        for num in range(7):
            week_day = today + timedelta(days=num)
            title = f"{week_day.strftime('%A')} {week_day.day} {week_day.strftime('%b')}"
            rows = self.session.query(Table).filter(Table.deadline == week_day.date()).all()
            self.tasks_print(title, rows, form=False)

    def all_tasks(self, today):
        rows = self.session.query(Table).\
            filter(Table.deadline >= today.date()).\
            order_by(Table.deadline).all()
        self.tasks_print("All tasks:", rows)

    def missed_tasks(self, today):
        rows = self.session.query(Table). \
            filter(Table.deadline < today.date()). \
            order_by(Table.deadline).all()
        self.tasks_print("Missed tasks:", rows, no_task="Nothing is missed!")

    def delete_task(self):
        rows = self.session.query(Table).\
            filter(Table.deadline).order_by(Table.deadline).all()
        title = "Choose the number of the task you want to delete:"
        self.tasks_print(title, rows, no_task="Nothing to delete")
        if rows:
            choice = int(input("> "))
            self.session.delete(rows[choice - 1])
            self.session.commit()
            print("The task has been deleted!")

    @staticmethod
    def tasks_print(title, rows, no_task="Nothing to do!", form=True):
        print(f"\n{title}:")
        if rows:
            for count, row in enumerate(rows, 1):
                if form:
                    print(f"{count}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                else:
                    print(f"{count}. {row.task}")
        else:
            print(f"{no_task}")


new_to_do = MyToDo("todo")
