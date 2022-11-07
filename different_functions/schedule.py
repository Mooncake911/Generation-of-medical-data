# ~Create schedule_data and concatenate with doctors_data~ #
import datetime as dt
import pandas as pd
import random


def create_schedule():
    list_of_schedules = []

    for i in range(50):
        schedule = []
        for j in range(7):
            star_day = dt.timedelta(hours=random.choices([7, 8, 9], weights=[0.3, 0.4, 0.3])[0],
                                    minutes=random.choices([0, 30, 45], weights=[0.3, 0.4, 0.3])[0])
            end_day = dt.timedelta(hours=random.choices([16, 17, 18], weights=[0.3, 0.4, 0.3])[0],
                                   minutes=random.choices([0, 30, 45], weights=[0.3, 0.4, 0.3])[0])

            schedule.append(str(star_day) + '-' + str(end_day))

        rest_days = 2
        for t in range(rest_days):
            rest_day = random.choices([0, 1, 2, 3, 4, 5, 6], weights=[0.1, 0.1, 0.2, 0.1, 0.1, 0.2, 0.2])[0]
            schedule[rest_day] = 'Нерабочий день'

        rest = random.choices(['12:00:00-12:30:00', '13:00:00-14:00:00', '15:00:00-15:30:00'], weights=[0.3, 0.4, 0.3])[0]
        schedule.append(rest)

        list_of_schedules.append(schedule)

    data = pd.read_csv('D:\\Projects\\PyCharm_Projects\\big_data\\Tables\\doctors_data.csv', sep=',', low_memory=False)
    data[['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Cб', 'Вс', 'Перерыв на обед']] = pd.DataFrame(list_of_schedules)
    data.to_csv('D:\\Projects\\PyCharm_Projects\\big_data\\Tables\\doctors_data.csv', index=False)
