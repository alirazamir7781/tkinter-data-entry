import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import array as arr
import numpy as np

def enter_data(value,first_name_entry,last_name_entry,title_combobox,age_spinbox,nationality_combobox,reg_status_var,numcourses_spinbox,numsemesters_spinbox):
    print(value.get())
    accepted = value.get()
    
    if accepted=="Accepted":
        # User info
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        
        if firstname and lastname:
            title = title_combobox.get()
            age = age_spinbox.get()
            nationality = nationality_combobox.get()
            
            # Course info
            registration_status = reg_status_var.get()
            numcourses = numcourses_spinbox.get()
            numsemesters = numsemesters_spinbox.get()
            
            print("First name: ", firstname, "Last name: ", lastname)
            print("Title: ", title, "Age: ", age, "Nationality: ", nationality)
            print("# Courses: ", numcourses, "# Semesters: ", numsemesters)
            print("Registration status", registration_status)
            print("------------------------------------------")
            
            # Create Table
            conn = sqlite3.connect('data.db')
            table_create_query = '''CREATE TABLE IF NOT EXISTS Student_Data 
                    (firstname TEXT, lastname TEXT, title TEXT, age INT, nationality TEXT, 
                    registration_status TEXT, num_courses INT, num_semesters INT)
            '''
            conn.execute(table_create_query)
            
            # Insert Data
            data_insert_query = '''INSERT INTO Student_Data (firstname, lastname, title, 
            age, nationality, registration_status, num_courses, num_semesters) VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?)'''
            data_insert_tuple = (firstname, lastname, title,
                                  age, nationality, registration_status, numcourses, numsemesters)
            cursor = conn.cursor()
            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit()
            conn.close()

            
                
        else:
            tkinter.messagebox.showwarning(title="Error", message="First name and last name are required.")
    else:
        tkinter.messagebox.showwarning(title= "Error", message="You have not accepted the terms")

def View_data():
    try:
        
        # Connect to the SQLite database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info(Student_Data)")
        columns=cursor.fetchall()
        columnname = np.array([column[1] for column in columns])
        #print (columnname)
        # Execute a SELECT query
        cursor.execute('SELECT firstname, lastname, title, age, nationality, registration_status, num_courses, num_semesters FROM Student_Data')
        rows = cursor.fetchall()
        #columnname=["firstname", "lastname", "title", "age", "nationality", "registration_status", "num_courses", "num_semesters"]
        # Display the retrieved data using Tkinter messagebox
        # messagebox.showinfo('Data from Database', '\n'.join(map(str, rows)))
        
        window = tkinter.Tk()
        window.title("Data View Form")
        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                label = tkinter.Label(window, text=f" {columnname[col_index]}")
                label.grid(row=row_index, column=2*col_index)

                entry = tkinter.Entry(window)
                entry.insert(tkinter.END, str(value))
                entry.grid(row=row_index, column=2*col_index+1)

        # Create a Tkinter Text widget to display the data
        #text_widget = tkinter.Text(window)
        #text_widget.pack()

        # Insert the retrieved data into the Text widget
        #for row in rows:
         #   text_widget.insert(tkinter.END, str(row) + '\n')
        def on_closing():
    # Open a new window when the main window is closed
            window.destroy()
            openwindow()
        
        
        

# Bind the closing event to the root window
        window.protocol("WM_DELETE_WINDOW", on_closing)
    # Run the Tkinter event loop
        #window.mainloop()
        # Run the Tkinter event loop
        #window.mainloop()

        # Close the database connection
        conn.close()
        #window.destroy()
        #openwindow()
        
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', str(e))

def on_click(window_handle):
    window_handle.destroy()
    View_data()
       
def openwindow():
    window = tkinter.Tk()
    window.title("Data Entry Form")

    frame = tkinter.Frame(window)
    frame.pack()

# Saving User Info
    user_info_frame =tkinter.LabelFrame(frame, text="User Information")
    user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

    first_name_label = tkinter.Label(user_info_frame, text="First Name")
    first_name_label.grid(row=0, column=0)
    last_name_label = tkinter.Label(user_info_frame, text="Last Name")
    last_name_label.grid(row=0, column=1)

    first_name_entry = tkinter.Entry(user_info_frame)
    last_name_entry = tkinter.Entry(user_info_frame)
    first_name_entry.grid(row=1, column=0)
    last_name_entry.grid(row=1, column=1)

    title_label = tkinter.Label(user_info_frame, text="Title")
    title_combobox = ttk.Combobox(user_info_frame, values=["", "Mr.", "Ms.", "Dr."])
    title_label.grid(row=0, column=2)
    title_combobox.grid(row=1, column=2)

    age_label = tkinter.Label(user_info_frame, text="Age")
    age_spinbox = tkinter.Spinbox(user_info_frame, from_=18, to=110)
    age_label.grid(row=2, column=0)
    age_spinbox.grid(row=3, column=0)
    nationality_label = tkinter.Label(user_info_frame, text="Nationality")
    nationality_combobox = ttk.Combobox(user_info_frame, values=["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America"])
    nationality_label.grid(row=2, column=1)
    nationality_combobox.grid(row=3, column=1)

    for widget in user_info_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

# Saving Course Info
    courses_frame = tkinter.LabelFrame(frame)
    courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    registered_label = tkinter.Label(courses_frame, text="Registration Status")

    reg_status_var = tkinter.StringVar(value="Not Registered")
    registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registered",
                                       variable=reg_status_var, onvalue="Registered", offvalue="Not registered")

    registered_label.grid(row=0, column=0)
    registered_check.grid(row=1, column=0)

    numcourses_label = tkinter.Label(courses_frame, text= "# Completed Courses")
    numcourses_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
    numcourses_label.grid(row=0, column=1)
    numcourses_spinbox.grid(row=1, column=1)

    numsemesters_label = tkinter.Label(courses_frame, text="# Semesters")
    numsemesters_spinbox = tkinter.Spinbox(courses_frame, from_=0, to="infinity")
    numsemesters_label.grid(row=0, column=2)
    numsemesters_spinbox.grid(row=1, column=2)

    for widget in courses_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

# Accept terms
    terms_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
    terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)
    #accept_var=tkinter.BooleanVar(value=False)
    accept_var = tkinter.StringVar(value="Not Accepted")
    terms_check = tkinter.Checkbutton(terms_frame, text= "I accept the terms and conditions.",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
    terms_check.grid(row=0, column=0)
    #accept_var.trace("w", lambda *args: get_checkbutton_value())
    
    
# Button
    button = tkinter.Button(frame, text="Enter data", command=lambda:enter_data(accept_var,first_name_entry,last_name_entry,title_combobox,age_spinbox,nationality_combobox,reg_status_var,numcourses_spinbox,numsemesters_spinbox))
    button.grid(row=3, column=0, sticky="news", padx=20, pady=10)
    button = tkinter.Button(frame, text="View data", command= lambda:on_click(window))
    button.grid(row=4, column=0, sticky="news", padx=20, pady=10)
 
    window.mainloop()
    


openwindow()