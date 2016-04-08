import threading
import Tkinter as tk
import ttk
import time
def foo():
    time.sleep(5) # simulate some work

def start_foo_thread(event):
    global foo_thread
    foo_thread = threading.Thread(target=foo)
    foo_thread.daemon = True
    progressbar.start()
    foo_thread.start()
    root.after(20, check_foo_thread)

def check_foo_thread():
    if foo_thread.is_alive():
        root.after(20, check_foo_thread)
    else:
        progressbar.stop()

root = tk.Tk()
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
progressbar = ttk.Progressbar(mainframe, mode='indeterminate')
progressbar.grid(column=1, row=100)

ttk.Button(mainframe, text="Check",command=lambda:start_foo_thread(None)).grid(column=1, row=200)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
root.bind('<Return>', start_foo_thread)

root.mainloop()
