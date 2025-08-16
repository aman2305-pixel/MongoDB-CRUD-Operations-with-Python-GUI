import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["student_db"]
collection = db["students"]

# Insert Data
def insert_data():
    name = entry_name.get()
    age = entry_age.get()
    course = entry_course.get()

    if name and age and course:
        collection.insert_one({"name": name, "age": int(age), "course": course})
        messagebox.showinfo("Success", "Record inserted successfully!")
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

# Read Data
def read_data():
    records = collection.find()
    text_area.delete(1.0, tk.END)
    for record in records:
        text_area.insert(tk.END, f"{record['_id']} - {record['name']} - {record['age']} - {record['course']}\n")

# Update Data (name, age, and course)
def update_data():
    search_name = entry_search_name.get()
    new_name = entry_name.get()
    new_age = entry_age.get()
    new_course = entry_course.get()

    if search_name and (new_name or new_age or new_course):
        update_fields = {}
        if new_name:
            update_fields["name"] = new_name
        if new_age:
            update_fields["age"] = int(new_age)
        if new_course:
            update_fields["course"] = new_course

        result = collection.update_one({"name": search_name}, {"$set": update_fields})

        if result.modified_count > 0:
            messagebox.showinfo("Success", "Record updated successfully!")
        else:
            messagebox.showwarning("Not Found", "No record found with that name.")
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please enter the name to search and at least one new value.")

# Delete Data
def delete_data():
    name = entry_name.get()

    if name:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Record deleted successfully!")
        else:
            messagebox.showwarning("Not Found", "No record found with that name.")
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please enter the name to delete.")

# Clear Entry Fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    entry_search_name.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("MongoDB CRUD with Python GUI (Full Update)")

# Search Field for Update
tk.Label(root, text="Search by Name (for Update):").grid(row=0, column=0)
entry_search_name = tk.Entry(root)
entry_search_name.grid(row=0, column=1)

# Labels & Entries for New Data
tk.Label(root, text="Name:").grid(row=1, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

tk.Label(root, text="Age:").grid(row=2, column=0)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1)

tk.Label(root, text="Course:").grid(row=3, column=0)
entry_course = tk.Entry(root)
entry_course.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Insert", command=insert_data).grid(row=4, column=0, pady=5)
tk.Button(root, text="Read", command=read_data).grid(row=4, column=1)
tk.Button(root, text="Update", command=update_data).grid(row=5, column=0)
tk.Button(root, text="Delete", command=delete_data).grid(row=5, column=1)

# Text Area
text_area = tk.Text(root, height=10, width=50)
text_area.grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop()