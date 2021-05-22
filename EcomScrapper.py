from tkinter import *

from sphinx.testing.path import path
from ttkthemes import themed_tk as tk
from tkinter import ttk
import csv
from sys import exit
import tkinter.messagebox
import time
import PaytmMall
import GeekBuying
import BolScrapping
import pathlib

app = tk.ThemedTk()
brand_name = StringVar()

# get data from csv and save to arrayList
tempList = []
path_ = 'C:/Users/Kastriot/Desktop/Ecommerce-Srcapper/venv/'
print(path_)

# label
key_word_label = ttk.Label(app, text="Click button to start scrapping data from websites: ", font=('bold', 12), padding=10)
key_word_label.grid(row=0, column=0, sticky=W)


# start scrapping on button click
def start_scrapping():
    print("Scrapping started.. please wait to download all products..")
    BolScrapping.start_scrapper()
    GeekBuying.start_scrapper()
    PaytmMall.start_scrapper()
    print("finish scrapping..")


# select on search box
def on_search_select(event):
    page_hint_text = 'Enter search'
    if pages_entry.get() == page_hint_text:
        pages_entry.delete(0, "end")  # delete all the text in the entry
        pages_entry.insert(0, '')


#  on search button click, will search for particular product from files
def search_items():
    brand_ = brand_name.get()
    # clear tree
    for i in listBox.get_children():
        listBox.delete(i)
    for i, (name, price, new_price, discount, brand, url) in enumerate(tempList, start=1):
        if brand == brand_ and name != 'not found':
            name = name.strip(" ").strip("\n").strip(" ")
            listBox.insert("", "end", values=(name, '$' + price, '$' + new_price, '$' + discount, brand, url))


#     get all data with discount
def search_discounts():
    # clear tree
    for i in listBox.get_children():
        listBox.delete(i)
    for i, (name, price, new_price, discount, brand, url) in enumerate(tempList, start=1):
        if discount != '0' and name != 'not found':
            name = name.strip(" ").strip("\n").strip(" ")
            listBox.insert("", "end", values=(name, '$' + price, '$' + new_price, '$' + discount, brand, url))


#        sort data in treeview
def treeview_sort_column(tv, col_, reverse):
    print('here')
    l_ = [(tv.set(k, col_), k) for k in tv.get_children('')]
    l_.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l_):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tv, col_, not reverse))


#     load all data from files
def show_all():
    time.sleep(2)
    # clear tree
    for i in listBox.get_children():
        listBox.delete(i)
    # load data from CSV and save to arrayList
    # try:
    with open(path_+'BolLaptops.csv', 'r', newline='', encoding='latin1') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] != 'not found':
                tempList.append(row)
    tempList.sort(key=lambda e: e[1], reverse=True)

    with open(path_+'BolMobiles.csv', 'r', newline='', encoding='latin1') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] != 'not found':
                tempList.append(row)
    tempList.sort(key=lambda e: e[1], reverse=True)

    with open(path_+'GeekLaptops.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] != 'not found':
                tempList.append(row)
    tempList.sort(key=lambda e: e[1], reverse=True)

    with open(path_+'GeekMobiles.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] != 'not found':
                tempList.append(row)
    tempList.sort(key=lambda e: e[1], reverse=True)

    with open(path_+'PaytmLaptops.csv', 'r', newline='', encoding='latin1') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] != 'not found':
                tempList.append(row)
    tempList.sort(key=lambda e: e[1], reverse=True)

    with open(path_+'PaytmMobiles.csv', 'r', newline='', encoding='latin1') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] != 'not found':
                tempList.append(row)
    tempList.sort(key=lambda e: e[1], reverse=True)

    for i, (name, price, new_price, discount, brand, url) in enumerate(tempList, start=1):
        name = name.strip(' ')
        if '€' in price:
            name = name.strip('\n\t').rstrip().strip(' ')
            listBox.insert("", "end", values=(name,  price, new_price, discount, brand, url))
        else:
            name = name.strip('\n\t').rstrip().strip(' ')
            listBox.insert("", "end", values=(name, '$' + price, '$' + new_price, '$' + discount, brand, url))
    # except:
    #     print("no file found..")


# click buttons for extracting data from web
start_scrapping_btn = ttk.Button(app, text='Start Scrapping', width=50, command=start_scrapping)
start_scrapping_btn.grid(row=0, column=1, sticky=W, pady=20)

# add edit text
pages_entry = ttk.Entry(app, textvariable=brand_name, width=50)
pages_entry.insert(0, 'Enter search')
pages_entry.bind('<FocusIn>', on_search_select)
pages_entry.grid(row=3, column=0)

# click buttons for search
search_btn = ttk.Button(app, text='Search', width=10, command=search_items)
search_btn.grid(row=3, column=1, sticky=W, pady=20)

# click buttons for discount
discount_btn = ttk.Button(app, text='Show all Products having Discount', width=50, command=search_discounts)
discount_btn.grid(row=4, column=0, pady=2)

# click buttons for discount
discount_btn = ttk.Button(app, text='Show All products', width=30, command=show_all)
discount_btn.grid(row=4, column=1, sticky=W, pady=2)


# Add listView TreeView to show all data from CSV, saved
cols = ('Name', 'Price', 'New Price', 'Discount', 'Brand', 'Url')
listBox = ttk.Treeview(app, columns=cols, show='headings')
# set column headings
for col in cols:
    listBox.heading(col, text=col, command=lambda _col=col: treeview_sort_column(listBox, _col, False))
listBox.grid(row=1, column=0, columnspan=5)

# display all data in listView tree
show_all()


app.get_themes()
app.set_theme("breeze")
app.title('E-Commerce Web Scrapper')
app.geometry('1030x450')

# start programme
app.mainloop()
