import random

groups = ["TTP1", "TTP2", "TTP3"]
rooms = ["Room1", "Room2", "Room3"]
# Часи
times = ["8:40-10:10", "10:35-12:10", "12:20-13:55"]
professors_info = {
    "Проф. Нікітченко Микола Степанович": {"office": "601", "subjects": ["формальні моделі програмування", "мови програмування та мови специфікацій", "формальні методи розробки програм", "логіка предикатів на різних рівнях абстракції", "абстрактна обчислювальність"], "max_hours": 3, "current_hours": 0},
    "Проф. Дорошенко Анатолій Юхимович": {"office": "602", "subjects": ["кластерні паралельні обчислення", "grid-технології і «хмарні» системи", "агентно-орієнтовані технології та засоби інтелектуалізації програмування", "крупномасшабні прикладні обчислення (метеорологія, екологія)", "автоматизація наукових досліджень"], "max_hours": 3, "current_hours": 0},
    "Проф. Шкільняк Степан Степанович": {"office": "608", "subjects": ["логіко-математичні засоби специфікацій програм", "математична логіка"], "max_hours": 3, "current_hours": 0},
    "Доц. Волохов Віктор Миколайович": {"office": "610", "subjects": ["системне програмування", "теорія та технології баз даних", "комп'ютерні мережі", "безпека інформації в комп'ютерних мережах"], "max_hours": 3, "current_hours": 0},
    "Доц. Зубенко Віталій Володимирович": {"office": "605", "subjects": ["основи інформатики та програмування", "програмні логіки", "інформаційне моделювання", "дистанційне навчання"], "max_hours": 3, "current_hours": 0},
    "Доц. Панченко Тарас Володимирович": {"office": "611", "subjects": ["композиційні методи", "інтернет-технології", "бази даних"], "max_hours": 3, "current_hours": 0},
    "Доц. Омельчук Людмила Леонідівна": {"office": "610", "subjects": ["формальні методи розробки програм", "технології програмування"], "max_hours": 3, "current_hours": 0},
    "Доц. Ткаченко Олексій Миколайович": {"office": "603", "subjects": ["технології програмування", "формальні методи розробки ПЗ", "освітні ІТ"], "max_hours": 3, "current_hours": 0},
    "Доц. Русіна Наталія Геннадіївна": {"office": "605", "subjects": ["формування інформатичних компетентностей", "розробка інформаційних систем для дистанційного навчання", "тестовий інструментарій", "дослідження методів специфікації та верифікації програмних систем"], "max_hours": 3, "current_hours": 0},
    "Асис. Криволап Андрій Володимирович": {"office": "612", "subjects": ["формальні методи", "верифікація програмного забезпечення", "програмні логіки", "теорія категорій"], "max_hours": 3, "current_hours": 0},
    "Асис. Белова Анна Сергіївна": {"office": "603", "subjects": [], "max_hours": 3, "current_hours": 0},
    "Асис. Поліщук Наталія Володимирівна": {"office": "603", "subjects": [], "max_hours": 3, "current_hours": 0},
    "Асис. Шишацька Олена Володимирівна": {"office": "604", "subjects": ["формальна розробка програм", "програмні алгебри", "багатозначні логіки"], "max_hours": 3, "current_hours": 0},
    "Асис. Свистунов Антон Олександрович": {"office": "606", "subjects": ["хмарні обчислення", "розподілені системи", "архітектура програмних систем", "технології програмування"], "max_hours": 3, "current_hours": 0}
}
# Дні тижня
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
# Оголошення списку teachers та ініціалізація його значеннями з professors_info.keys()
teachers = list(professors_info.keys())
# Оголошення та ініціалізація словника teacher_subjects
teacher_subjects = {teacher: info["subjects"] for teacher, info in professors_info.items()}



def csp_algorithm():
    schedule = {}
    for group in groups:
        for weekday in weekdays:
            for time in times:
                available_professors = [professor for professor, info in professors_info.items() if info["subjects"]]
                random.shuffle(available_professors)
                professor_assigned = False

                for professor in available_professors:
                    if professors_info[professor]["subjects"]:
                        subject = random.choice(professors_info[professor]["subjects"])

                        for room in rooms:
                            room_occupied = any(
                                value[2] == room
                                for key, value in schedule.items()
                                if key[1] == weekday and key[2] == time
                            )

                            if not room_occupied:
                                if professors_info[professor]["current_hours"] < professors_info[professor]["max_hours"]:
                                    schedule[(group, weekday, time)] = (professor, subject, room)
                                    professors_info[professor]["current_hours"] += 1
                                    professor_assigned = True
                                    break

                    if professor_assigned:
                        break

                if not professor_assigned:

                    pass
    return schedule


def heuristic(schedule):
    cost = 0
    return cost



def print_schedule(schedule):
    for weekday in weekdays:
        print(f"\n{weekday}:")
        for key in sorted(schedule):
            if key[1] == weekday:
                professor, subject, room = schedule[key]
                office = professors_info[professor]["office"]
                print(f"Group: {key[0]}, Time: {key[2]}, Professor: {professor}, Subject: {subject}, Room : {office}")

schedule = csp_algorithm()
print_schedule(schedule)
