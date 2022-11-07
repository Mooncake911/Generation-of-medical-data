# -*- coding: utf-8 -*-
""" ~ The sample ~ """
from memory_profiler import memory_usage
import different_functions as df
import datetime as dt
import pandas as pd
import random


def main():
    person_list = []

    for person_id in range(0, df.amount_of_patients):
        visits = random.randint(5, 10)  # How many times client visited hospital
        person = df.get_fio()
        passport = df.get_passport(person_id)
        snils = df.get_snils(person_id)
        wallet = df.get_methods(person_id, visits)

        person_get_results = df.start_date
        for v in range(visits):
            idx, doctor = df.get_doctor()
            person_symptoms = df.get_symptoms(idx)
            person_come = df.get_visit(idx, person_get_results)
            med_tests, bill = df.get_analysis_and_bill(idx)
            person_get_results = df.get_analysis_ready(person_come)
            paid = wallet[v]

            person_list.append(
                [person, passport, snils, person_come, person_symptoms, doctor, med_tests, person_get_results, bill,
                 paid])

            person_get_results += dt.timedelta(days=1)  # Person can return to the hospital only after 24h

    data = pd.DataFrame(person_list)
    data.columns = ['Имя Фамилия', 'Паспортные данные', 'Снилс', 'Дата регистрации', 'Симптомы и болезни',
                    'Лечащий врач', 'Анализы', 'Время получения анализов', 'Чек в ₽', 'Оплачено']
    data.to_csv('Tables\\data.csv', index=False)


if __name__ == '__main__':
    main()
    print(memory_usage())
