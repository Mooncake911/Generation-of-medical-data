import time
import pandas as pd
from pycanon import anonymity
from sklearn.utils import shuffle
from faker import Faker
fake = Faker('ru_RU')

# Input
k_counter = 10  # Necessary k-anonymity counter

start_time = time.time()
data = pd.read_parquet("D:\\Projects\\PyCharm_Projects\\big_data\\Tables\\Parquet\\data.parquet", engine='pyarrow')
time_columns = ['Время получения анализов', 'Дата регистрации']
data[time_columns] = data[time_columns].astype('datetime64[ns]')  # Stupid panda don't definite type datetime


def main():
    def med_aggregation():
        data1 = pd.DataFrame()
        doctors = list(set(data['Лечащий врач']))
        symptoms = [set() for _ in range(len(doctors))]
        med_tests = [set() for _ in range(len(doctors))]
        for n in range(len(data['Лечащий врач'])):
            symptoms[doctors.index(data['Лечащий врач'][n])].update(set(data['Симптомы и болезни'][n].split(',')))
            med_tests[doctors.index(data['Лечащий врач'][n])].update(set(data['Анализы'][n].split(',')))
        data1['Доктора'] = pd.Series(doctors).astype('category')
        data1['Наиболее встречающаяся симптоматика'] = pd.Series(symptoms)
        data1['Наиболее встречающиеся анализы'] = pd.Series(med_tests)
        data1.to_csv('Tables\\statistics.csv', index=False)
        data1.to_parquet('Tables\\Parquet\\statistics.parquet', index=False)

    def hide_date(t):
        """ Local generalization for date """
        if 9 <= t <= 11:
            return "осень"
        elif 3 <= t <= 5:
            return "весна"
        elif 6 <= t <= 8:
            return "лето"
        else:
            return "зима"

    # Local suppression save in "statistics.parquet"
    med_aggregation()
    data.drop(data[data['Оплачено с'] == 'наличными'].index, inplace=True)
    del_list = ['Паспортные данные', 'Снилс', 'Симптомы и болезни', 'Анализы', 'Время получения анализов']
    data.drop(columns=del_list, axis=1, inplace=True)

    # Shuffle + Masking for pay method
    data['Оплачено с'] = data['Оплачено с'].apply(lambda x: str(x)[:1] + '*** **** **** ****').astype('category')
    data['Оплачено с'] = shuffle(data['Оплачено с'])

    # Shuffle + Masking for bill (rounding)
    '''y + (1000 - y % 1000)'''
    data['Чек в ₽'] = data['Чек в ₽'].apply(lambda y: y + 1000 - y % 1000).astype('category')
    data['Чек в ₽'] = shuffle(data['Чек в ₽'])

    # Shuffle + Local generalization
    data['Дата регистрации'] = data['Дата регистрации'].apply(lambda z: hide_date(z.month)).astype('category')
    data['Дата регистрации'] = shuffle(data['Дата регистрации'])

    # Fake information
    data['ФИО'] = data['ФИО'].apply(lambda w: fake.first_name())

    # Count k-anonymity
    QI = ['Дата регистрации', 'Лечащий врач', 'Чек в ₽', 'Оплачено с']
    k_initial, k_arr = anonymity.k_anonymity(data, QI)  # k-anonymity and array of unique rows 
    count_rows = 0
    for i in range(len(k_arr)):
        if len(k_arr[i]) < k_counter:
            for j in range(len(k_arr[i])):
                data.drop(k_arr[i][j], inplace=True)
                count_rows += 1
    k_final, k_arr = anonymity.k_anonymity(data, QI)

    # Outputting information
    print("%s rows were deleted to reach" % count_rows)
    print("%s -> %s your k-anonymity" % (k_initial, k_final))
    print("%s current size of data-set" % (data.size//len(data.columns)))

    data.to_csv('Tables\\anonymity_data.csv', index=False)
    data.to_parquet('Tables\\Parquet\\anonymity_data.parquet', index=False)


if __name__ == '__main__':
    main()
    print("%s seconds" % (time.time() - start_time))
