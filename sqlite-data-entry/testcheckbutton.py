import tkinter as tk
root = tk.Tk()

# Create a boolean variable to track the check button's state
is_accepted = tk.BooleanVar(value=False)

def on_checkbutton_toggle():
    # Toggle the state of the check button
    is_accepted.set(is_accepted.get())
    # Retrieve the current value based on the check button's state
    value = "Accepted" if is_accepted.get() else "Not Accepted"
    print(value)

# Create a check button
terms_check = tk.Checkbutton(root, text="I accept the terms and conditions.",
                             variable=is_accepted, onvalue=True, offvalue=False,
                             command=on_checkbutton_toggle)
terms_check.pack()

# Run the Tkinter event loop
root.mainloop()