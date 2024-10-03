from threading import Thread
from random import randint
from time import sleep
from queue import Queue


class Table:
    def __init__(self, number, guest=None):
        self.number = number
        self.guest = guest


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self) -> None:
        waiting = randint(3, 10)
        sleep(waiting)


class Cafe:
    list_table_rent = []

    def __init__(self, *tables: Table):
        self.tables = list(tables)
        self.queue = Queue()

    def guest_arrival(self, *guests: Guest) -> None:
        list_guests = list(guests)
        list_tables = self.tables
        minimal_count = min(len(list_guests), len(self.tables))
        for i in range(minimal_count):
            list_tables[i].guest = guests[i]
            table_rent = guests[i]
            table_rent.start()
            Cafe.list_table_rent.append(table_rent)
            print(f'{list_guests[i].name} сел(-а) за стол номер {list_tables[i].number}')
        if len(list_guests) > minimal_count:
            for i in range(minimal_count, len(list_guests)):
                self.queue.put(guests[i])
                print(f'{list_guests[i].name} в очереди')

    def check_table(self) -> bool:
        for table in self.tables:
            if table.guest is not None:
                return True
        return False

    def discuss_guests(self) -> None:
        while not (self.queue.empty()) or Cafe.check_table(self):
            for table in self.tables:
                if not (table.guest is None) and not (table.guest.is_alive()):
                    print(f'{table.guest.name} покушал(-а) и ушел(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                if (not (self.queue.empty())) and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    table_rent = table.guest
                    table_rent.start()
                    Cafe.list_table_rent.append(table_rent)


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
