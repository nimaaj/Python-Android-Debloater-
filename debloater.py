import subprocess
import tkinter as tk
from tkinter import messagebox

# Define the command to get packages list
def get_packages():
    output = subprocess.check_output("adb shell pm list packages --user 0", shell=True)
    output = output.decode("utf-8")
    package_list = output.split('\n')
    package_list = [pkg.replace('package:', '') for pkg in package_list if pkg]
    package_list.sort()
    return package_list

# Define the command to uninstall packages
# Define the command to uninstall packages
def uninstall_packages():
    selected_packages = listbox.curselection()
    for pkg in reversed(selected_packages):  # reversed to avoid shifting indices
        pkg_name = listbox.get(pkg)
        uninstall_command = f'adb shell pm uninstall --user 0 {pkg_name}'
        try:
            output = subprocess.check_output(uninstall_command, shell=True, stderr=subprocess.STDOUT)
            output_text.insert(tk.END, f'\n{output.decode()}')
            listbox.delete(pkg)  # remove package from list
        except subprocess.CalledProcessError as e:
            output_text.insert(tk.END, f'\n{e.output.decode()}')
    output_text.insert(tk.END, 'Selected packages uninstalled successfully.')




root = tk.Tk()

# Add a variable and an entry box for the filter
filter_var = tk.StringVar(root)
filter_entry = tk.Entry(root, textvariable=filter_var)
filter_entry.pack()

# Create listbox
listbox = tk.Listbox(root, selectmode='multiple')
listbox.pack(pady=20)
listbox.pack(fill=tk.BOTH, expand=1)


# Update the listbox whenever the filter changes
def update_listbox(*args):
    search_term = filter_var.get()
    listbox.delete(0, tk.END)
    for pkg in packages:
        if search_term.lower() in pkg.lower():
            listbox.insert(tk.END, pkg)
filter_var.trace('w', update_listbox)
# Fetch and insert packages into the listbox
packages = get_packages()
for pkg in packages:
    listbox.insert(tk.END, pkg)

# Create uninstall button
uninstall_button = tk.Button(root, text='Uninstall Selected', command=uninstall_packages)
uninstall_button.pack(pady=20)

# Create output text box
output_text = tk.Text(root, bg='black', fg='white')
output_text.pack()

root.mainloop()
