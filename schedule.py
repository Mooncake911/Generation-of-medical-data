# Create schedule_data and concatenate with doctors_profiles

import datetime as dt
import pandas as pd
import random

list_of_schedules = []

for i in range(45):
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

data = pd.DataFrame(list_of_schedules)
data.columns = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Cб', 'Вс', 'Перерыв на обед']
data.to_csv('Tables/schedule_data.csv', index=False)

df1 = pd.read_csv("Tables/doctors_profiles.csv", sep=',', low_memory=False)
df2 = pd.read_csv("Tables/schedule_data.csv", sep=',')
data = pd.concat([df1, df2], sort=False, axis=1)
data.to_csv('Tables/doctors_data.csv', index=False)
