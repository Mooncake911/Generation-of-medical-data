# """ ~Useful functions to great medical data-set~ """ #
from different_functions.schedule import create_schedule
from different_functions.input import get_input
from numba import prange
import datetime as dt
import pandas as pd
import random

# Global values
amount_of_patients = 1000
start_date = dt.datetime.strptime('01/01/2022', '%m/%d/%Y')  # When the hospital was founded
analyses_hours = ('10:00:00', '17:00:00')  # The period when person can get his analyses
chance_women = 0.3
chance_men = 0.7
chance_rf = 0.85
chance_bel = 0.1
chance_kz = 0.05
chance_cash = 0.1
chance_mir = 0.3
chance_mastercard = 0.4
chance_visa = 0.2
chance_ftime = 0.6
chance_stime = 0.4
get_input()

# Unique values
rf_passports = random.sample(prange(1000000000, 9999999999), amount_of_patients)
bel_origin = ('АВ', 'ВМ', 'НВ', 'КН', 'МР', 'МС', 'КБ', 'ПП')
bel_passports = random.sample(prange(1000000, 9999999), amount_of_patients)
kz_passports = random.sample(prange(100000000000, 999999999999), amount_of_patients)
sn_ls = random.sample(prange(10000000000, 99999999999), amount_of_patients)
cards = random.sample(prange(100000000000, 999999999999), 2 * amount_of_patients)

# Use different data_bases to create my own
# 1
fio_df = pd.read_csv("D:\\Projects\\PyCharm_Projects\\big_data\\Tables\\russian_names.csv", sep=',')
surnames = fio_df['Surname'][0:382]
names = fio_df['Name'][0:]
sex = fio_df['Sex'][0:]
consonants = str.split('б в г д ж з к л м н п р с т ф х ц ч ш щ')

# 2
create_schedule()
doc_df = pd.read_csv("D:\\Projects\\PyCharm_Projects\\big_data\\Tables\\doctors_data.csv", sep=',', low_memory=False)
doctors = doc_df['Doctors'][0:50]
doc_description = [str.split(doc_df['Description'][i], ',') for i in prange(50)]
doc_analyses = [str.split(doc_df['Analysis'][i], ',') for i in prange(50)]


def get_fio():
    """Return name, surname, second name"""
    # Girls (0, 23732) and Boys (23732...)
    # Choose name: Girls 30% and Boys 70% for our person
    name_gender = random.choices(('Ж', 'М'), weights=[chance_women, chance_men])[0]
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
    """Return rf, bel or kz passport"""
    rf_passport = '{0}{1}{2}'.format(str(rf_passports[t])[:4], " ", str(rf_passports[t])[4:])
    bel_passport = '{0}{1}'.format(str(random.choice(bel_origin)), str(bel_passports[t]))
    kz_passport = str(kz_passports[t])
    return random.choices([rf_passport, bel_passport, kz_passport], weights=[chance_rf, chance_bel, chance_kz])[0]


def get_snils(t):
    """Return sn_ils. It's uniform for each person who wants to get medical help in Russia"""
    return str(sn_ls[t])[:3] + "-" + str(sn_ls[t])[3:-5] + "-" + str(sn_ls[t])[6:-2] + "-" + str(sn_ls[t])[9:]


def get_card(t):
    """Return pay system and bank"""
    # Cash, Mir, Mastercard, Visa
    system = random.choices(('0', '2', '4', '5'), weights=[chance_cash, chance_mir, chance_mastercard, chance_visa])[0]
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


def get_methods(t, kol):
    """First 5 times are the person's usual payment, the rest are new one"""
    methods = []
    usual_card = get_card(t)  # Person's usual payment
    for i in prange(kol):
        if i < 5:
            methods.append(usual_card)
        else:
            methods.append(get_card(random.randint(amount_of_patients, 2 * amount_of_patients - 1)))
    random.shuffle(methods)
    return methods


def get_doctor():
    """Return doctor"""
    idx = random.randint(0, len(doctors) - 1)
    return idx, doctors[idx]


def get_symptoms(i):
    """Return random person's symptoms, according to doc_description"""
    count_of_symptoms = random.randint(1, len(doc_description[i]))
    symptoms = set(
        doc_description[i][random.randint(0, len(doc_description[i]) - 1)] for _ in prange(count_of_symptoms))
    return symptoms


def get_visit(i, previous_visit):
    """Choose day and time from a schedule to understand when the person can visit the doctor[i]"""
    schedule = doc_df.loc[i, ['Cб', 'Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Перерыв на обед']]
    at_day = 'Нерабочий день'
    i = 0
    while at_day == 'Нерабочий день':
        i = random.randint(0, 6)
        at_day = schedule[i]
    # print(i)
    w_hours = at_day.split('-')  # doctor work hours, example 9:00-17:00
    r_hours = schedule[7].split('-')  # doctor rest hours, example 12:00-13:00
    first_part_of_day = visit_time(w_hours[0], r_hours[0])
    second_part_of_day = visit_time(r_hours[1], w_hours[1])

    time = random.choices([first_part_of_day, second_part_of_day], weights=[chance_ftime, chance_stime])[0]
    date = visit_date(previous_visit, i) + dt.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)

    return date


def visit_date(previous_visit, week_day):
    """Find correct date"""
    def find_day_of_week(date):
        """day of week = (day +  moth_code + year_code) % 7"""
        year_code = (6 + (date.year % 100) + (date.year % 100) // 4) % 7
        month_code = 7
        match date.month:
            case 1 | 10:
                month_code = 1
            case 5:
                month_code = 2
            case 8:
                month_code = 3
            case 2 | 3 | 11:
                month_code = 4
            case 6:
                month_code = 5
            case 9 | 12:
                month_code = 6
            case 4 | 7:
                month_code = 0
        return (date.day + month_code + year_code) % 7

    rand_date = previous_visit + dt.timedelta(weeks=random.randrange(0, 5), days=random.randrange(0, 7))
    while find_day_of_week(rand_date) != week_day:
        rand_date += dt.timedelta(days=1)
    return rand_date


def visit_time(ot, do):
    """Choose random time in the interval |ot:do| = ot + delta <= do"""
    delta = str(dt.datetime.strptime(do, '%H:%M:%S') - dt.datetime.strptime(ot, '%H:%M:%S')).split(':')
    if int(delta[0]) == 0:  # Special condition when work period 15:30 to 16:00
        minutes = int(delta[1])
        hours = 1
    else:
        hours = int(delta[0])
        minutes = 60
    return dt.datetime.strptime(ot, '%H:%M:%S') + dt.timedelta(hours=random.randrange(0, hours),
                                                               minutes=random.randrange(0, minutes),
                                                               seconds=random.randint(0, 60))


def get_analysis_and_bill(i):
    """Return analyses and the sum of their prices"""
    count_of_analyses = random.randint(1, len(doc_analyses[i]))
    analyses = set(doc_analyses[i][random.randint(0, len(doc_analyses[i]) - 1)] for _ in prange(count_of_analyses))
    price = sum(random.randint(250, 1000) for _ in prange(count_of_analyses))
    return analyses, price


def get_analysis_ready(when_was_the_visit):
    """Analysis will be ready during two days"""
    date = when_was_the_visit + dt.timedelta(days=random.randrange(0, 2), hours=random.randrange(0, 24),
                                             minutes=random.randrange(0, 60), seconds=random.randint(0, 60))
    return date
