# -*- coding: utf-8 -*-

from numba import prange
import datetime as dt
import pandas as pd
import random


def get_fio():
    # Girls (0, 23732) and Boys (23732...)
    # Choose name: Girls 30% and Boys 70% for our person
    name_gender = random.choices(('Ж', 'М'), weights=[0.3, 0.7])[0]
    if name_gender == 'Ж':
        name = str(names[random.randint(0, 23732)])
        surname = str(surnames[random.randint(0, len(surnames) - 1)]) + 'a'
        second_name = str(names[random.randint(23732, len(names) - 1)])
        if second_name[-1] in consonants:
            second_name += 'овна'
        if second_name[-1] == 'ь' or second_name[-1] == 'й':
            second_name += 'евна'
        else:
            second_name += 'ична'
    else:
        name = str(names[random.randint(23732, len(names) - 1)])
        surname = str(surnames[random.randint(0, len(surnames) - 1)])
        second_name = str(names[random.randint(23732, len(names) - 1)])
        if second_name[-1] in consonants:
            second_name += 'ович'
        if second_name[-1] == 'ь' or second_name[-1] == 'й':
            second_name += 'евич'
        else:
            second_name += 'ич'
    return '{0}{1}{2}{3}{4}'.format(name, " ", surname, " ", second_name)


def get_passport(t):
    rf_passport = '{0}{1}{2}'.format(str(rf_passports[t])[:4], " ", str(rf_passports[t])[4:])
    bel_passport = '{0}{1}'.format(str(random.choice(bel_origin)), str(bel_passports[t]))
    kz_passport = str(kz_passports[t])
    return random.choices([rf_passport, bel_passport, kz_passport], weights=[0.85, 0.1, 0.05])[0]


def get_s_nils(t):
    # It's uniform for each person who wants to get medical help in Russia
    return str(sn_ls[t])[:3] + "-" + str(sn_ls[t])[3:-5] + "-" + str(sn_ls[t])[6:-2] + "-" + str(sn_ls[t])[9:]


def get_card(t):
    # Cash, Mir, Mastercard, Visa
    system = random.choices(('0', '2', '4', '5'), weights=[0.1, 0.3, 0.4, 0.2])[0]
    unique_code = '{0}{1}{2}{3}{4}'.format(str(cards[t])[:4], " ", str(cards[t])[4:-4], " ", str(cards[t])[8:])
    # Sberbank, Tinkoff, Opening
    match system:
        case '0':
            return 'наличными'
        case '2':
            bank = '200'
            return '{0}{1}{2}{3}'.format(system, bank, " ", unique_code)
        case '4':
            bank = random.choices(('276', '377', '093'), weights=[0.45, 0.35, 0.2])[0]
            return '{0}{1}{2}{3}'.format(system, bank, " ", unique_code)
        case '5':
            bank = random.choices(('336', '213', '323'), weights=[0.45, 0.35, 0.2])[0]
            return '{0}{1}{2}{3}'.format(system, bank, " ", unique_code)


def get_methods(kol, t):
    methods = []
    usual_card = get_card(t)  # Person's usual payment
    for i in prange(kol):
        if i < 5:
            methods.append(usual_card)
        else:
            methods.append(get_card(random.randint(amount_of_patients, 2*amount_of_patients-1)))
    random.shuffle(methods)
    return methods


def get_analysis_and_bill():
    doctor_recommend = []
    # Индекс должен принадлежать доктору
    a_index = random.randint(0, len(analyses) - 1)
    analysis_list = str.split(analyses[a_index], ',')
    kol = random.randint(1, len(analysis_list))
    while kol:
        i = random.randint(0, len(analysis_list)-1)
        doctor_recommend.append(analysis_list[i])
        kol -= 1
    doctor_recommend = set(doctor_recommend)
    price = sum(random.randint(250, 1000) for _ in prange(len(doctor_recommend)))
    return doctor_recommend, price


def get_analysis_ready(when_was_the_visit):
    # Analysis will be ready during two days
    date = when_was_the_visit + dt.timedelta(days=random.randint(0, 1), hours=random.randint(0, 23),
                                             minutes=random.randint(0, 59), seconds=random.randint(0, 60))
    return date


def get_random_date(start, end):
    delta = end - start
    steps = str.split(str(delta), ':')
    if int(steps[0]) > 1:
        hours = random.randrange(0, int(steps[0]))
    else:
        hours = 0
    return start + dt.timedelta(weeks=random.randint(0, 7), days=random.randint(0, 30),
                                hours=hours, minutes=random.randint(0, 59),
                                seconds=random.randint(0, 60))


def visit_time(l_visit, start, end):
    ot = l_visit.strftime('%m/%d/%Y:') + start
    do = l_visit.strftime('%m/%d/%Y:') + end
    part_of_day = get_random_date(dt.datetime.strptime(ot, '%m/%d/%Y:%H:%M:%S'),
                                  dt.datetime.strptime(do, '%m/%d/%Y:%H:%M:%S'))
    return part_of_day


def when_the_person_come(w_hours, r_hours, date_visit):
    # The chance that a person will come in the first part of the day is 60%, in the second 40%
    first_part_of_day = visit_time(date_visit, w_hours[0], r_hours[0])
    second_part_of_day = visit_time(date_visit, r_hours[1], w_hours[1])
    return random.choices([first_part_of_day, second_part_of_day], weights=[0.6, 0.4])[0]


def what_worries_the_person():
    count_of_symptoms = random.randint(1, 10)
    person_symptoms = set(illnesses[random.randint(0, len(illnesses) - 1)] for _ in prange(count_of_symptoms))
    return person_symptoms


def choose_doctor_and_get_his_schedule(person_symptoms):
    person_doctor = "you have cancer"
    max_coincidences = 0
    d_idx = 0
    for i in prange(0, len(doctors) - 1):
        k = len(person_symptoms & set(doc_description[i]))
        if k >= max_coincidences:
            max_coincidences = k
            person_doctor = doctors[i]
            d_idx = i
    schedule = doc_df.loc[d_idx, ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Cб', 'Вс', 'Перерыв на обед']]
    return person_doctor, schedule


def which_day_doctor_work(schedule):
    in_day = schedule[random.randint(0, 6)]
    while in_day == 'Нерабочий день':
        in_day = schedule[random.randint(0, 6)]
    return in_day


def main():
    x = 0
    interval = 100000  # Writing to file every 100 000 lines
    while x < amount_of_patients:
        if x + interval > amount_of_patients:
            interval = amount_of_patients - x
        person_list = []
        # print(x, x+interval)
        for person_id in prange(x, x + interval):
            person = get_fio()
            passport = get_passport(person_id)
            s_nils = get_s_nils(person_id)

            visits = random.randint(5, 10)  # How many times person visited hospital
            paid_methods = get_methods(visits, person_id)
            results_came = start_date
            for v in prange(visits):
                symptoms = what_worries_the_person()
                doctor, doctor_schedule = choose_doctor_and_get_his_schedule(symptoms)

                visit_day = which_day_doctor_work(doctor_schedule)  # example: Monday
                doctor_work_hours = visit_day.split('-')  # example: 9:00-17:00
                doctor_rest_hours = doctor_schedule[7].split('-')  # example: 12:00-13:00
                visit = when_the_person_come(doctor_work_hours, doctor_rest_hours, results_came)  # 10:15 or 14:25

                med_tests, bill = get_analysis_and_bill()
                results_came = get_analysis_ready(visit)
                paid = paid_methods[v]

                person_list.append([person, passport, s_nils, visit, symptoms, doctor, med_tests, results_came, bill, paid])

                results_came += dt.timedelta(days=1)

        x = x + interval

        data = pd.DataFrame(person_list)
        data.columns = ['Имя Фамилия', 'Паспортные данные', 'Снилс', 'Дата регистрации', 'Симптомы и болезни',
                        'Лечащий врач', 'Анализы', 'Время получения анализов', 'Чек в ₽', 'Оплачено']
        data.to_csv('data.csv', index=False)


if __name__ == '__main__':
    # Global values
    amount_of_patients = 10000
    start_date = dt.datetime.strptime('01/01/2022:', '%m/%d/%Y:')  # When the hospital was founded
    analyses_hours = ('10:00:00', '17:00:00')  # The period when person can get his analyses

    rf_passports = random.sample(prange(1000000000, 9999999999), amount_of_patients)
    bel_origin = ('АВ', 'ВМ', 'НВ', 'КН', 'МР', 'МС', 'КБ', 'ПП')
    bel_passports = random.sample(prange(1000000, 9999999), amount_of_patients)
    kz_passports = random.sample(prange(100000000000, 999999999999), amount_of_patients)
    sn_ls = random.sample(prange(10000000000, 99999999999), amount_of_patients)
    cards = random.sample(prange(100000000000, 999999999999), 2 * amount_of_patients)

    # Use different data_bases to create my own
    # 1
    fio_df = pd.read_csv("Tables/russian_names.csv", sep=',')
    surnames = fio_df['Surname'][0:382]
    names = fio_df['Name'][0:]
    sex = fio_df['Sex'][0:]
    consonants = str.split('б в г д ж з к л м н п р с т ф х ц ч ш щ')

    # 2
    med_df = pd.read_csv("Tables/medical_data.csv", sep=',', low_memory=False)
    illnesses = med_df['Symptoms and diseases'][0:196]

    # 3
    doc_df = pd.read_csv("Tables/doctors_data.csv", sep=',', low_memory=False)
    doctors = doc_df['Doctors'][0:45]
    doc_description = [str.split(doc_df['Description'][i], ',') for i in prange(45)]
    analyses = doc_df['Analysis'][0:9]

    main()
