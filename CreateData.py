# -*- coding: utf-8 -*-
""" ~ The sample ~ """
from memory_profiler import memory_usage
import different_functions as fd
import datetime as dt
import random
import pandas as pd
import time
start_time = time.time()


def get_person_row(person_id):
    person_list = []
    visits = random.randint(5, 10)  # How many times client visited hospital
    person = fd.get_fio()
    passport = fd.get_passport(person_id)
    snils = fd.get_snils(person_id)
    wallet = fd.get_methods(person_id, visits)
    person_get_results = fd.start_date
    for v in range(visits):
        idx, doctor = fd.get_doctor()
        person_symptoms = fd.get_symptoms(idx)
        person_come = fd.get_visit(idx, person_get_results)
        med_tests, bill = fd.get_analysis_and_bill(idx)
        person_get_results = fd.get_analysis_ready(person_come)
        paid = wallet[v]
        person_list.append([person, passport, snils, person_come, person_symptoms, doctor, med_tests, person_get_results, bill, paid])
        person_get_results += dt.timedelta(days=1)  # Person can return to the hospital only after 24h
    return person_list


def main():
    persons_list = []
    for person_id in range(0, fd.amount_of_patients):
        row = get_person_row(person_id)
        for i in range(len(row)):
            persons_list.append(row[i])

    data = pd.DataFrame(persons_list)
    data.columns = ['ФИО', 'Паспортные данные', 'Снилс', 'Дата регистрации', 'Симптомы и болезни',
                    'Лечащий врач', 'Анализы', 'Время получения анализов', 'Чек в ₽', 'Оплачено с']
    data.to_csv('Tables\\data.csv', index=False)
    data.to_parquet('Tables\\Parquet\\data.parquet', index=False)
    del persons_list, row


if __name__ == '__main__':
    main()
    print("%s seconds" % (time.time() - start_time))
    print("%s megabyte" % memory_usage()[0])
