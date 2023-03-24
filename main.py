import tkinter as tk

root = tk.Tk()
root.title("Tu bedzie super ekstra gierka")
root.geometry("400x300")
root.configure(bg='yellow')

label = tk.Label(root, text="KWICINEK")
label.pack()

root.mainloop()
