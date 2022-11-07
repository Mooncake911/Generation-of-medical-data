import different_functions.get_fun as df
from tkinter import *
import datetime as dt


def get_input():
    def clicked():
        try:
            df.amount_of_patients = int(input_people.get())
            df.start_date = dt.datetime.strptime(input_start_date.get(), '%m/%d/%Y')

            df.chance_women = float(input_girls.get())
            df.chance_men = float(input_boys.get())

            df.chance_rf = float(input_rf.get())
            df.chance_bel = float(input_bel.get())
            df.chance_kz = float(input_kz.get())

            df.chance_cash = float(input_cash.get())
            df.chance_mir = float(input_mir.get())
            df.chance_mastercard = float(input_mastercard.get())
            df.chance_visa = float(input_visa.get())

            df.chance_ftime = float(input_fpart.get())
            df.chance_stime = float(input_spart.get())

            window.destroy()
        except:
            warning_window = Tk()
            warning_window.title('Error')
            warning_window['bg'] = 'red'
            warning_window.geometry('200x50')
            Label(warning_window, text="Данные введене не корректно", bg='red').grid(column=0, row=0)

    window = Tk()
    window.title('Parameters for creating data-base')
    window.geometry('500x500')

    Label(window, text="Введите данные для заполнения таблицы:").grid(column=0, row=0)

    Label(window, text="Количество пациентов:").grid(column=0, row=1)
    input_people = Entry(window, width=20)
    input_people.grid(column=1, row=1)
    input_people.insert(0, '1000')

    Label(window, text="Дата начала записей:").grid(column=0, row=2)
    input_start_date = Entry(window, width=20)
    input_start_date.grid(column=1, row=2)
    input_start_date.insert(0, '01/01/2022')

    Label(window, text="% посещения женщин: 0.0->1.0").grid(column=0, row=3)
    input_girls = Entry(window, width=20)
    input_girls.grid(column=1, row=3)
    input_girls.insert(0, '0.3')

    Label(window, text="% посещения мужчин: 0.0->1.0").grid(column=0, row=4)
    input_boys = Entry(window, width=20)
    input_boys.grid(column=1, row=4)
    input_boys.insert(0, '0.7')

    Label(window, text="% посещения граждан России: 0.0->1.0").grid(column=0, row=5)
    input_rf = Entry(window, width=20)
    input_rf.grid(column=1, row=5)
    input_rf.insert(0, '0.85')

    Label(window, text="% посещения граждан Белоруссии: 0.0->1.0").grid(column=0, row=6)
    input_bel = Entry(window, width=20)
    input_bel.grid(column=1, row=6)
    input_bel.insert(0, '0.1')

    Label(window, text="% посещения граждан Казахстана: 0.0->1.0").grid(column=0, row=7)
    input_kz = Entry(window, width=20)
    input_kz.grid(column=1, row=7)
    input_kz.insert(0, '0.05')

    Label(window, text="% людей оплачивающих наличными: 0.0->1.0").grid(column=0, row=8)
    input_cash = Entry(window, width=20)
    input_cash.grid(column=1, row=8)
    input_cash.insert(0, '0.1')

    Label(window, text="% людей оплачивающих картой Мир: 0.0->1.0").grid(column=0, row=9)
    input_mir = Entry(window, width=20)
    input_mir.grid(column=1, row=9)
    input_mir.insert(0, '0.3')

    Label(window, text="% людей оплачивающих картой Mastercard: 0.0->1.0").grid(column=0, row=10)
    input_mastercard = Entry(window, width=20)
    input_mastercard.grid(column=1, row=10)
    input_mastercard.insert(0, '0.4')

    Label(window, text="% людей оплачивающих картой Visa: 0.0->1.0").grid(column=0, row=11)
    input_visa = Entry(window, width=20)
    input_visa.grid(column=1, row=11)
    input_visa.insert(0, '0.2')

    Label(window, text="% людей приходящих на приём в 1 половине дня: 0.0->1.0").grid(column=0, row=12)
    input_fpart = Entry(window, width=20)
    input_fpart.grid(column=1, row=12)
    input_fpart.insert(0, '0.6')

    Label(window, text="% людей приходящих на приём во 2 половине дня: 0.0->1.0").grid(column=0, row=13)
    input_spart = Entry(window, width=20)
    input_spart.grid(column=1, row=13)
    input_spart.insert(0, '0.4')

    btn = Button(window, text="Создать дата-сет", command=clicked)
    btn.grid(column=0, row=15)

    window.mainloop()
