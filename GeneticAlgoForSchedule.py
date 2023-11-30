import random

# Припустимо, що у нас є деякі викладачі, предмети, групи та аудиторії

groups = ["TTP1", "TTP2", "TTP3"]
rooms = ["Room1", "Room2", "Room3"]
professors_info = {
    "Проф. Нікітченко Микола Степанович": {"office": "601", "subjects": ["формальні моделі програмування", "мови програмування та мови специфікацій", "формальні методи розробки програм", "логіка предикатів на різних рівнях абстракції", "абстрактна обчислювальність"], "max_hours": 3, "current_hours": 0},
    "Проф. Дорошенко Анатолій Юхимович": {"office": "602", "subjects": ["кластерні паралельні обчислення", "grid-технології і «хмарні» системи", "агентно-орієнтовані технології та засоби інтелектуалізації програмування", "крупномасшабні прикладні обчислення (метеорологія, екологія)", "автоматизація наукових досліджень"], "max_hours": 3, "current_hours": 0},
    "Проф. Шкільняк Степан Степанович": {"office": "611", "subjects": ["логіко-математичні засоби специфікацій програм", "математична логіка"], "max_hours": 3, "current_hours": 0},
    "Доц. Волохов Віктор Миколайович": {"office": "611", "subjects": ["системне програмування", "теорія та технології баз даних", "комп'ютерні мережі", "безпека інформації в комп'ютерних мережах"], "max_hours": 3, "current_hours": 0},
    "Доц. Зубенко Віталій Володимирович": {"office": "603", "subjects": ["основи інформатики та програмування", "програмні логіки", "інформаційне моделювання", "дистанційне навчання"], "max_hours": 3, "current_hours": 0},
    "Доц. Панченко Тарас Володимирович": {"office": "611", "subjects": ["композиційні методи", "інтернет-технології", "бази даних"], "max_hours": 3, "current_hours": 0},
    "Доц. Омельчук Людмила Леонідівна": {"office": "611", "subjects": ["формальні методи розробки програм", "технології програмування"], "max_hours": 3, "current_hours": 0},
    "Доц. Ткаченко Олексій Миколайович": {"office": "603", "subjects": ["технології програмування", "формальні методи розробки ПЗ", "освітні ІТ"], "max_hours": 3, "current_hours": 0},
    "Доц. Русіна Наталія Геннадіївна": {"office": "603", "subjects": ["формування інформатичних компетентностей", "розробка інформаційних систем для дистанційного навчання", "тестовий інструментарій", "дослідження методів специфікації та верифікації програмних систем"], "max_hours": 3, "current_hours": 0},
    "Асис. Криволап Андрій Володимирович": {"office": "611", "subjects": ["формальні методи", "верифікація програмного забезпечення", "програмні логіки", "теорія категорій"], "max_hours": 3, "current_hours": 0},
    "Асис. Белова Анна Сергіївна": {"office": "603", "subjects": [], "max_hours": 3, "current_hours": 0},
    "Асис. Поліщук Наталія Володимирівна": {"office": "603", "subjects": [], "max_hours": 3, "current_hours": 0},
    "Асис. Шишацька Олена Володимирівна": {"office": "603", "subjects": ["формальна розробка програм", "програмні алгебри", "багатозначні логіки"], "max_hours": 3, "current_hours": 0},
    "Асис. Свистунов Антон Олександрович": {"office": "603", "subjects": ["хмарні обчислення", "розподілені системи", "архітектура програмних систем", "технології програмування"], "max_hours": 3, "current_hours": 0}
}

# Часи
times = ["8:40-10:10", "10:35-12:10", "12:20-13:55"]

# Дні тижня
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Кожен розклад - це словник, де ключ - це пара (група, день, час), а значення - це пара (викладач, предмет, аудиторія)
def create_schedule():
    schedule = {}
    for group in groups:
        for weekday in weekdays:
            for time in times:
                professor = random.choice(list(professors_info.keys()))

                if professors_info[professor]["subjects"]:
                    subject = random.choice(professors_info[professor]["subjects"])

                    room = random.choice(rooms)

                    if not any(value[0] == professor for key, value in schedule.items() if
                               key[1] == weekday and key[2] == time):

                        if professors_info[professor]["current_hours"] < professors_info[professor]["max_hours"]:
                            schedule[(group, weekday, time)] = (professor, subject, room)

                            professors_info[professor]["current_hours"] += 1

    return schedule


# Функція оцінки якості розкладу
def heuristic(schedule):
    cost = 0
    return cost

# Генетичний алгоритм
def genetic_algorithm():
    population = [create_schedule() for _ in range(100)]  # Створення початкової популяції
    for _ in range(1000):  # Кількість ітерацій
        population.sort(key=heuristic)  # Сортування популяції за оцінкою якості
        population = population[:20]  # Відбір найкращих особин
        for _ in range(80):  # Створення нового покоління
            schedule1 = random.choice(population)
            schedule2 = random.choice(population)
            child = crossover(schedule1, schedule2)  # Створення нового розкладу шляхом схрещування
            mutate(child)  # Мутація нового розкладу
            population.append(child)
    return min(population, key=heuristic)  # Повернення найкращого розкладу

# Схрещування двох розкладів
def crossover(schedule1, schedule2):
    child = schedule1.copy()
    for key in schedule1:
        if key in schedule2 and random.random() < 0.5:
            child[key] = schedule2[key]
    return child

# Мутація розкладу
def mutate(schedule):
    if not schedule:
        return

    key_to_mutate = random.choice(list(schedule.keys()))
    teacher = random.choice(teachers)
    subject = random.choice(teacher_subjects[teacher])
    room = random.choice(rooms)

    # Перевірка, чи викладач вже має заняття в цей час і на цьому дні
    if not any(value[0] == teacher for key, value in schedule.items() if
               key[1] == key_to_mutate[1] and key[2] == key_to_mutate[2]):
        schedule[key_to_mutate] = (teacher, subject, room)


# Виведення розкладу
def print_schedule(schedule):
    for weekday in weekdays:
        print(f"\n{weekday}:")
        for key in sorted(schedule):
            if key[1] == weekday:
                professor, subject, room = schedule[key]
                office = professors_info[professor]["office"]
                print(f"Group: {key[0]}, Time: {key[2]}, Professor: {professor}, Subject: {subject}, Room : {office}")

schedule = genetic_algorithm()
print_schedule(schedule)
