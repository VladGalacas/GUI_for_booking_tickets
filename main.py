import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd

from tkinter import messagebox as mb
from database import make_df, execute_query
from tkcalendar import DateEntry


def booking(
        root,
        spin,
        count_tickets_event_information,
        age_limit_event_information,
        price_event_information,
        event_information_df,
        event_information_id_now,
        destroy_main_root):
    try:
        choise_count_tickets = int(spin.get())
        if choise_count_tickets < 1:
            mb.showerror('Ошибка', 'Вы не можете забронировать меньше одного билета!')
        elif choise_count_tickets > count_tickets_event_information:
            mb.showerror('Ошибка', 'Вы не можете забронировать больше билетов, чем есть в наличии!')
        else:
            if age_limit_event_information != 0:
                age_answer = mb.askyesno(title='Возрастное ограничения',
                                         message=f'Вам больше {age_limit_event_information} лет?')
                if age_answer:
                    mb.showinfo(title='Бронь',
                                message=f'Забронировано билетов: {choise_count_tickets} шт.'
                                        f'\nИх общая стоимость: {price_event_information * choise_count_tickets} руб.')
                    count_tickets_event_information_now = count_tickets_event_information - choise_count_tickets
                    event_information_df['count_tickets'].where(~(event_information_df.id == event_information_id_now),
                                                                count_tickets_event_information_now, inplace=True)
                    execute_query(
                        f"UPDATE event_information SET count_tickets = {count_tickets_event_information_now} "
                        f"WHERE id = {event_information_id_now};")
                    root.destroy()
                    if destroy_main_root:
                        root1.destroy()
                else:
                    mb.showerror(title='Ошибка',
                                 message='Вы не проходите по возрастному ограничению, выберете другое мероприятие!')
            else:
                mb.showinfo(title='Бронь',
                            message=f'Забронировано билетов: {choise_count_tickets} шт.'
                                    f'\nИх общая стоимость: {price_event_information * choise_count_tickets} руб.')
                count_tickets_event_information_now = count_tickets_event_information - choise_count_tickets
                event_information_df['count_tickets'].where(
                    ~(event_information_df.id == event_information_id_now),
                    count_tickets_event_information_now, inplace=True)
                execute_query(
                    f"UPDATE event_information SET count_tickets = {count_tickets_event_information_now} "
                    f"WHERE id = {event_information_id_now};")
                root.destroy()
    except ValueError:
        mb.showerror('Ошибка', 'Введите численное значение кол-ва билетов!')


def start_select(root,
                 shift_grid,
                 event_information_df,
                 type_event_df,
                 type_leisure_df,
                 date_event_for_select,
                 destroy_main_root):
    def get_type_leisure(event):

        def get_type_event(event):

            def get_event_information(event):

                event_information_id_now = \
                    event_information_df[event_information_df['name_event'] == event_information_combo.get()][
                        'id'].to_list()[0]
                if date_event_for_select:
                    date_event_information = \
                        event_information_df[event_information_df['id'] == event_information_id_now][
                            'date_event'].to_list()[0]
                else:
                    date_event_information = \
                        event_information_df[event_information_df['id'] == event_information_id_now][
                            'date_event'].to_list()[0].strftime('%d.%m.%Y')
                time_event_information = \
                    event_information_df[event_information_df['id'] == event_information_id_now][
                        'time_event'].to_list()[
                        0].strftime('%H:%M')
                price_event_information = \
                    event_information_df[event_information_df['id'] == event_information_id_now]['price'].to_list()[0]
                count_tickets_event_information = \
                    event_information_df[event_information_df['id'] == event_information_id_now][
                        'count_tickets'].to_list()[
                        0]
                age_limit_event_information = \
                    event_information_df[event_information_df['id'] == event_information_id_now]['age_limit'].to_list()[
                        0]

                if count_tickets_event_information == 0:
                    mb.showwarning(title='Закончились билеты',
                                   message='Вы не можете забронировать билеты, т.к. в наличии их не осталось!')
                else:
                    if date_event_for_select:
                        tk.Label(root, text=f'\nВремя: {time_event_information}'
                                            f'\nЦена: {price_event_information} руб.'
                                            f'\nКол-во имеющихся билетов: {count_tickets_event_information}'
                                            f'\nВозрастное ограничение: {age_limit_event_information}+').grid(
                            column=3 + shift_grid, row=1 + shift_grid)
                    else:
                        tk.Label(root, text=f'Дата: {date_event_information}'
                                            f'\nВремя: {time_event_information}'
                                            f'\nЦена: {price_event_information} руб.'
                                            f'\nКол-во имеющихся билетов: {count_tickets_event_information}'
                                            f'\nВозрастное ограничение: {age_limit_event_information}+').grid(
                            column=3 + shift_grid, row=1 + shift_grid)

                    tk.Label(root, text='Выберете кол-во билетов').grid(column=3 + shift_grid, row=2 + shift_grid)
                    spin = tk.Spinbox(root, width=4, from_=1, to=count_tickets_event_information)
                    spin.grid(column=3 + shift_grid, row=4 + shift_grid)
                    ttk.Button(root, text="Подтвердить бронирование", command=lambda: booking(root,
                                                                                              spin,
                                                                                              count_tickets_event_information,
                                                                                              age_limit_event_information,
                                                                                              price_event_information,
                                                                                              event_information_df,
                                                                                              event_information_id_now,
                                                                                              destroy_main_root)).grid(
                        column=3 + shift_grid, row=5 + shift_grid)

            type_event_id_now = \
                type_event_df[type_event_df['type_event_name'] == type_event_combo.get()]['id'].to_list()[0]
            tk.Label(root, text="Выберите событие").grid(column=2 + shift_grid, row=shift_grid)
            event_information_values = event_information_df[event_information_df['type_event_id'] == type_event_id_now][
                'name_event'].to_list()
            event_information_combo = ttk.Combobox(root, values=event_information_values, state='readonly',
                                                   width=len(
                                                       max(event_information_df['name_event'], key=lambda x: len(x))))
            event_information_combo.grid(column=2 + shift_grid, row=1 + shift_grid)
            event_information_combo.bind('<<ComboboxSelected>>', get_event_information)

        type_leisure_id_now = type_leisure_df[type_leisure_df['leisure'] == type_leisure_combo.get()]['id'].to_list()[0]
        tk.Label(root, text="Выберите вид события").grid(column=1 + shift_grid, row=shift_grid)
        type_event_values = type_event_df[type_event_df['type_leisure_id'] == type_leisure_id_now][
            'type_event_name'].to_list()
        type_event_combo = ttk.Combobox(root, values=type_event_values, state='readonly',
                                        width=len(
                                            max(type_event_df['type_event_name'].to_list(), key=lambda x: len(x))))
        type_event_combo.grid(column=1 + shift_grid, row=1 + shift_grid)
        type_event_combo.bind('<<ComboboxSelected>>', get_type_event)

    tk.Label(root, text="Выберите место проведения мероприятия").grid(column=shift_grid, row=shift_grid)
    type_leisure_values = type_leisure_df['leisure'].to_list()
    type_leisure_combo = ttk.Combobox(root, values=type_leisure_values, state='readonly',
                                      width=len(max(type_leisure_values, key=lambda x: len(x))))
    type_leisure_combo.grid(column=shift_grid, row=1 + shift_grid)
    type_leisure_combo.bind('<<ComboboxSelected>>', get_type_leisure)


def data_search():
    def show_sel():

        select_date_for_event_information_df_new = cal.get_date()
        selected_date = select_date_for_event_information_df_new.strftime('%Y-%m-%d')

        count_tickets_selected_date = event_information_df[event_information_df['date_event'] == selected_date][
            'count_tickets'].to_list()
        if len(count_tickets_selected_date) > 1 and len(
                [item for item in count_tickets_selected_date if item != 0]) > 0:

            # event_information
            name_event_selected_date = event_information_df[event_information_df['date_event'] == selected_date][
                'name_event'].to_list()
            time_event_selected_date = event_information_df[event_information_df['date_event'] == selected_date][
                'time_event'].to_list()
            price_event_selected_date = event_information_df[event_information_df['date_event'] == selected_date][
                'price'].to_list()
            age_limit_selected_date = event_information_df[event_information_df['date_event'] == selected_date][
                'age_limit'].to_list()
            type_event_id_selected_date = event_information_df[event_information_df['date_event'] == selected_date][
                'type_event_id'].to_list()

            # type_event
            type_event_name_selected_date_list, type_leisure_id_selected_date_list = [], []
            for id in type_event_id_selected_date:
                type_event_name_selected_date = type_event_df[type_event_df['id'] == id]['type_event_name'].to_list()
                type_event_name_selected_date_list += type_event_name_selected_date

                type_leisure_id_selected_date = type_event_df[type_event_df['id'] == id]['type_leisure_id'].to_list()
                type_leisure_id_selected_date_list += type_leisure_id_selected_date

            # type_leisure
            type_leisure_leisure_selected_date_list = []
            for id in type_leisure_id_selected_date_list:
                type_leisure_leisure_selected_date = type_leisure_df[type_leisure_df['id'] == id]['leisure'].to_list()
                type_leisure_leisure_selected_date_list += type_leisure_leisure_selected_date

            type_leisure_id_df_new = pd.DataFrame({'id': type_leisure_id_selected_date_list,
                                                   'leisure': type_leisure_leisure_selected_date_list})
            type_event_df_new = pd.DataFrame({'id': type_event_id_selected_date,
                                              'type_event_name': type_event_name_selected_date_list,
                                              'type_leisure_id': type_leisure_id_selected_date_list})
            event_information_df_new = pd.DataFrame({'id': range(1, len(name_event_selected_date) + 1),
                                                     'name_event': name_event_selected_date,
                                                     'date_event': select_date_for_event_information_df_new,
                                                     'time_event': time_event_selected_date,
                                                     'price': price_event_selected_date,
                                                     'count_tickets': count_tickets_selected_date,
                                                     'age_limit': age_limit_selected_date,
                                                     'type_event_id': type_event_id_selected_date})

            start_select(top, shift_grid=1, event_information_df=event_information_df_new,
                         type_event_df=type_event_df_new, type_leisure_df=type_leisure_id_df_new,
                         date_event_for_select=True, destroy_main_root=True)


        elif len(count_tickets_selected_date) == 0 or len(
                [item for item in count_tickets_selected_date if item != 0]) == 0:
            mb.showerror('Нет билетов', 'На данный день билетов ни на одно мероприятие нет!')

        elif len(count_tickets_selected_date) == 1 and len(
                [item for item in count_tickets_selected_date if item != 0]) == 1:

            # event_information
            name_event_selected_date = \
                event_information_df[event_information_df['date_event'] == selected_date]['name_event'].to_list()[0]
            time_event_selected_date = \
                event_information_df[event_information_df['date_event'] == selected_date]['time_event'].to_list()[
                    0].strftime('%H:%M')
            price_event_selected_date = \
                event_information_df[event_information_df['date_event'] == selected_date]['price'].to_list()[0]
            age_limit_selected_date = \
                event_information_df[event_information_df['date_event'] == selected_date]['age_limit'].to_list()[0]
            type_event_id_selected_date = \
                event_information_df[event_information_df['date_event'] == selected_date]['type_event_id'].to_list()[0]
            id_selected_date = \
                event_information_df[event_information_df['date_event'] == selected_date]['id'].to_list()[0]

            # type_event
            type_event_name_selected_date = \
                type_event_df[type_event_df['id'] == type_event_id_selected_date]['type_event_name'].to_list()[0]
            type_leisure_id_selected_date = \
                type_event_df[type_event_df['id'] == type_event_id_selected_date]['type_leisure_id'].to_list()[0]

            # type_leisure
            type_leisure_leisure_selected_date = \
                type_leisure_df[type_leisure_df['id'] == type_leisure_id_selected_date]['leisure'].to_list()[0]

            tk.Label(top, text=f'Место проведения мероприятия: {type_leisure_leisure_selected_date}'
                               f'\nВид события: {type_event_name_selected_date}'
                               f'\nНазвание события: {name_event_selected_date}'
                               f'\nВремя: {time_event_selected_date}'
                               f'\nЦена: {price_event_selected_date} руб.'
                               f'\nКол-во имеющихся билетов: {count_tickets_selected_date[0]}'
                               f'\nВозрастное ограничение: {age_limit_selected_date}+').grid(column=1, row=0)

            tk.Label(top, text='Выберете кол-во билетов').grid(column=1, row=1)
            spin = tk.Spinbox(top, width=4, from_=1, to=count_tickets_selected_date[0])
            spin.grid(column=1, row=2)
            ttk.Button(top, text="Подтвердить бронирование", command=lambda: booking(top,
                                                                                     spin,
                                                                                     count_tickets_selected_date[0],
                                                                                     age_limit_selected_date,
                                                                                     price_event_selected_date,
                                                                                     event_information_df,
                                                                                     id_selected_date,
                                                                                     destroy_main_root=True)).grid(
                column=1, row=3)

    top = tk.Toplevel()
    # top.geometry('213x115')
    # top.resizable(True, True)
    top.title('Поиск')

    tk.Label(top, text='Поиск по дате события').grid(column=0, row=0)
    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='dd.mm.y')
    cal.grid(column=0, row=1)
    ttk.Button(top, text='Выбрать', command=show_sel).grid(column=0, row=2)


if __name__ == '__main__':
    type_leisure_df, type_event_df, event_information_df = make_df()

    root1 = tk.Tk()
    # root1.geometry('1150x200')
    # root1.resizable(True, True)
    root1.title('Культурные мероприятия')

    start_select(root1, shift_grid=0, event_information_df=event_information_df, type_event_df=type_event_df,
                 type_leisure_df=type_leisure_df, date_event_for_select=False, destroy_main_root=False)

    ttk.Button(root1, text='Поиск по дате события', command=data_search).grid(column=0, row=5)
    root1.mainloop()
