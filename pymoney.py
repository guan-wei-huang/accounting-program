import sys
import tkinter
import tkinter.ttk as ttk
from pyrecord import Record
from pyrecord import Records
from pycategory import Categories

categories = Categories()
records = Records()

########################################
root = tkinter.Tk()
root.title('PyMoney')
f = tkinter.Frame(root , borderwidth = 5)
f.grid(row = 0, column = 0)

########################################
find_category = tkinter.Label(f, text = 'Find category')
find_category.grid(row = 0, column = 0, columnspan = 3)

find_str = tkinter.StringVar()
find_entry = tkinter.Entry(f, textvariable = find_str)
find_entry.grid(row = 0, column = 3, columnspan = 3)


def find_cate():
    category = find_str.get()
    target_categories = categories.find_subcategories(category)
    L = records.find(target_categories)
    result_box.delete(0, tkinter.END)
    surplus = 0
    for i in range(len(L)):
        surplus = surplus + int(L[i].amount)
        note = '{:<12s}{:<15s}{:<16s}{:<10d}'.format( L[i].date , L[i].category , L[i].description , L[i].amount )
        result_box.insert(i, note)
    display = 'Total amount above is ' + str(surplus) + ' dollars.'
    left_money_str.set(display)

find_button = tkinter.Button(f, text = 'Find', command = find_cate)
find_button.grid(row = 0, column = 6)

def Reset():
    L = records.records
    money = records.initial_money
    result_box.delete(0, tkinter.END)
    for i in range(len(L)):
        money = money + L[i].amount
        note = '{:<12s}{:<15s}{:>16s}{:>10d}'.format( L[i].date , L[i].category , L[i].description , L[i].amount )
        result_box.insert(i, note)
    display = 'Now you have ' + str(money) + ' dollars.'
    left_money_str.set(display)

reset_button = tkinter.Button(f, text = 'Reset', command = Reset)
reset_button.grid(row = 0, column = 7)

#######################################
initial_money = tkinter.Label(f, text = 'Initial money')
initial_money.grid(row = 0, column = 8)

initial_str = tkinter.StringVar()
initial_entry = tkinter.Entry(f, textvariable = initial_str)
initial_entry.grid(row = 0, column = 9, columnspan = 3)

def update_initial():
    money = initial_str.get()
    records.change_initial(int(money))
    display = 'Now you have ' + str(money) + ' dollars.'
    left_money_str.set(display)
    Reset()

initial_update = tkinter.Button(f, text = 'Update', command = update_initial)
initial_update.grid(row = 1, column = 11)

#########################################
date_label = tkinter.Label(f, text = 'Date')
date_label.grid(row = 2, column = 8)

date_str = tkinter.StringVar()
date_entry = tkinter.Entry(f, textvariable = date_str)
date_entry.grid(row = 2, column = 9, columnspan = 3)

category_label = tkinter.Label(f, text = 'Category')
category_label.grid(row = 3, column = 8)

cate = categories.view()
category_choose = ttk.Combobox(f, values = cate)
category_choose.grid(row = 3, column = 9, columnspan = 3)


description_label = tkinter.Label(f, text = 'Description')
description_label.grid(row = 4, column = 8)

description_str = tkinter.StringVar()
description_entry = tkinter.Entry(f, textvariable = description_str)
description_entry.grid(row = 4, column = 9, columnspan = 3)


amount_label = tkinter.Label(f, text = 'Amount')
amount_label.grid(row = 5, column = 8)

amount_str = tkinter.StringVar()
amount_entry = tkinter.Entry(f, textvariable = amount_str)
amount_entry.grid(row = 5, column = 9, columnspan = 3)


def add_record():
    date = date_str.get()
    category = cate[category_choose.current()]
    try:
        category = (category.split('- '))[1]
    except:
        category = (category.split('- '))[0]
    descri = description_str.get()
    amount = amount_str.get()
    record = str(date) + ' ' + str(category) + ' ' + str(descri) + ' ' + str(amount)
    records.add(record, categories)
    Reset()

add_record = tkinter.Button(f, text = 'Add a record', command = add_record)
add_record.grid(row = 6, column = 10, columnspan = 2)

aaa = tkinter.Label(f, text = 'Demo')
aaa.grid(row = 7 , column = 10) 
#########################################
result_box = tkinter.Listbox(f)
result_box.grid(row = 1, column = 0, rowspan = 5, columnspan = 5)
result_box.config(width = 0)


left_money_str = tkinter.StringVar()
begin_money = 'Now you have ' + str(records.initial_money) + ' dollars.'
left_money_str.set(begin_money)
left = tkinter.Label(f, textvariable=left_money_str, justify=tkinter.LEFT)
left.grid(row = 6, column = 0, columnspan = 6)

def delete(Listbox):
    selection = result_box.curselection()
    result_box.delete(selection[0])
    del records._records[selection[0]]
    Reset()


delete_button = tkinter.Button(f, text = 'Delete', command = lambda:delete(result_box))
delete_button.grid(row = 6, column = 7)

Reset()
tkinter.mainloop()
records.save()
