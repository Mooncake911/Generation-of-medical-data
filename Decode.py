import pandas as pd


def main():
    data = pd.read_csv('./Tables/Hack/student.csv', sep=',')
    email = data['email']
    address = data['Адрес']

    hacked_data = pd.read_csv('./Tables/Hack/hacked.txt')
    hacked_ph_num = hacked_data['Телефон']
    size = len(hacked_ph_num)

    for i in range(size):
        some_value = str(hacked_ph_num[i]).split(':')
        idx = data[data['Телефон'] == some_value[0]].index
        data.loc[idx, '1'] = some_value[1]

        words = address[i].replace('.', ' ').split()
        kv = words[len(words) - 2]
        shift = ord(kv[0]) - ord('к')
        if shift < 0:
            shift += 32

        # Key
        data.loc[i, 'Key'] = shift

        # Address
        add = address[i].lower()
        add = add.translate({ord(j): ord(j) - shift for j in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'})
        data.loc[i, '2'] = add.lower()

        # Email
        eml = email[i].translate({ord(j): ord(j) - shift for j in 'abcdefghijklmnopqrstuvwxyz'})
        eml = eml.translate({ord(j): ord(j) - 6 for j in "][^_\`ABCDEFGHIJKLMNOPQRSTUVWXYZ"})
        data.loc[i, '3'] = eml.lower()

    data.to_csv('Tables\\Hack\\student.csv', index=False)


if __name__ == '__main__':
    main()
