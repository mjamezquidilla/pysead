from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from turtle import clear
import customtkinter as ctk
import pandas as pd

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title('PySEAD')
root.geometry('800x800')

# Create Tabs
nodes_notebook = ttk.Notebook(root)
nodes_notebook.pack(pady=15)


# Create Treeview Frame
tree_view_frame = Frame(nodes_notebook) 
tree_view_frame.pack(pady=20) 

# Treeview Scrollbar
tree_scrollbar = Scrollbar(tree_view_frame)
tree_scrollbar.pack(side=RIGHT, fill=Y)
 
# Treeview
my_tree = ttk.Treeview(tree_view_frame, yscrollcommand=tree_scrollbar.set)
tree_scrollbar.config(command=my_tree.yview)

# Pack to Screen
my_tree.pack(pady=20)

global count
count = 0

# Define Columns
my_tree['columns'] = ("Name", "ID", "Food")

# Format the Columns
my_tree.column('#0', width=0, stretch=NO)
my_tree.column('Name', anchor=W, width=120, stretch=NO)
my_tree.column('ID', anchor=CENTER, width=120)
my_tree.column('Food', anchor=E, width=120)

# Create headings
my_tree.heading('#0')
my_tree.heading('Name', text=' Full Name', anchor=CENTER)
my_tree.heading('ID', text='ID', anchor=CENTER)
my_tree.heading('Food', text='Food', anchor=CENTER)


# Labels
add_frame = ctk.CTkFrame(master=root,
                               width=1000,
                               height=200)
add_frame.pack(pady=20)

n1 = ctk.CTkLabel(master=add_frame, text="Name")
n1.grid(row=0,column=0)


il = ctk.CTkLabel(master=add_frame, text="ID")
il.grid(row=0,column=1)

tl = ctk.CTkLabel(master=add_frame, text="Food")
tl.grid(row=0,column=2)

# Entry boxes
name_box = ctk.CTkEntry(master=add_frame)
name_box.grid(row=1, column=0)

id_box = ctk.CTkEntry(master=add_frame)
id_box.grid(row=1, column=1)

food_box = ctk.CTkEntry(master=add_frame)
food_box.grid(row=1, column=2)

# Buttons
def Add_Record():
    # Add record
    global count
    my_tree.insert(parent='', index='end', iid=count, text='parent', values=(name_box.get(),id_box.get(),food_box.get()))
    count += 1

    # Clear text boxes
    name_box.delete(0,END)
    id_box.delete(0,END)
    food_box.delete(0,END)

    my_tree.yview_moveto('1.0')

def Remove_All_Record():
    for record in my_tree.get_children():
        my_tree.delete(record)

def Remove_selected_record():
    x = my_tree.selection()
    for i in x:
        my_tree.delete(i)
    
    my_tree.yview_moveto('1.0')

def Select_Record():
    # clear entry boxes
    name_box.delete(0,END)
    id_box.delete(0,END)
    food_box.delete(0,END)

    # Grab Record number
    selected = my_tree.focus()

    # Grab record values
    values = my_tree.item(selected, 'values')

    # output to entry boxes
    name_box.insert(0,values[0])
    id_box.insert(0,values[1])
    food_box.insert(0,values[2])

def update_record():
    selected = my_tree.focus()
    my_tree.item(selected, text="", values=(name_box.get(),id_box.get(), food_box.get()))

    # clear entry boxes
    name_box.delete(0,END)
    id_box.delete(0,END)
    food_box.delete(0,END)

def file_open():
    filename = filedialog.askopenfilename(
                initialdir="C:/",
                title="Open CSV file",
                filetypes=(('CSV file','*.csv'),('all files','*.*'))
                )

    if filename:
        try:
            filename = r"{}".format(filename)
            df = pd.read_csv(filename)
        except ValueError:
            pass
    
    # Clear old tree view
    clear_tree()

    # Setup new tree view
    my_tree["column"] = list(df.columns)
    my_tree["show"] = "headings"

    # Loop through column lists for headers
    for column in my_tree["column"]:
        my_tree.heading(column, text=column)
    
    # Put data in treeview
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        my_tree.insert('','end', values=row)

    # pack tree view
    my_tree.pack()


def clear_tree():
    my_tree.delete(*my_tree.get_children())

Add_record = ctk.CTkButton(master=root, text="Add Record", command=Add_Record)
Remove_all_record = ctk.CTkButton(master=root, text="Remove All Record", command=Remove_All_Record)
Remove_selected_record = ctk.CTkButton(master=root, text="Remove Record", command=Remove_selected_record)
Select_Record = ctk.CTkButton(master=root, text="Select Record", command=Select_Record)
update_record = ctk.CTkButton(master=root, text="Update Record", command=update_record)
file_open = ctk.CTkButton(master=root, text="Open CSV File", command=file_open)

Add_record.pack()
Remove_all_record.pack()
Remove_selected_record.pack()
Select_Record.pack()
update_record.pack()
file_open.pack()


nodes_notebook.add(tree_view_frame, text='Nodes')

root.mainloop()