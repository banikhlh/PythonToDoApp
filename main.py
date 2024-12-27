import sqlite3
import tkinter

conn = None

def startApp():
    global conn
    conn = sqlite3.connect('toDo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE toDos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            task TEXT,
            status TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
                ''')
    conn.commit()
    load_toDos()

def closeApp():
    global conn
    if conn:
        conn.close()
    window.destroy()


def load_toDos():
    listbox.delete(0, tkinter.END)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, status FROM toDos")
    tasks = cursor.fetchall()
    for task in tasks:
        status = "✔️" if task[2] == "done" else "❌"
        listbox.insert(tkinter.END, f"{task[0]}. {status} {task[1]}")


def add_task():
    task = toDo_entry.get()
    if task.strip():
        cursor = conn.cursor()
        cursor.execute("INSERT INTO toDos (task, status) VALUES (?, ?)", (task, "pending"))
        conn.commit()
        toDo_entry.delete(0, tkinter.END)
        load_toDos()
    else:
        tkinter.messagebox.showwarning("Ошибка", "Введите текст задачи!")


def delete_task():
    try:
        selected = listbox.get(listbox.curselection())
        toDo_id = int(selected.split('.')[0])
        cursor = conn.cursor()
        cursor.execute("DELETE FROM toDos WHERE id = ?", (toDo_id,))
        conn.commit()
        load_toDos()
    except:
        tkinter.messagebox.showwarning("Ошибка", "Выберите задачу для удаления!")


def mark_done():
    try:
        selected = listbox.get(listbox.curselection())
        toDo_id = int(selected.split('.')[0])
        cursor = conn.cursor()
        cursor.execute("UPDATE toDos SET status = ? WHERE id = ?", ("done", toDo_id))
        conn.commit()
        load_toDos()
    except:
        tkinter.messagebox.showwarning("Ошибка", "Выберите задачу для выполнения!")


window = tkinter.Tk()
window.title("To Do List")
window.resizable(True, True)

toDo_entry = tkinter.Entry(window, width=30)
toDo_entry.pack(pady=10)

add_button = tkinter.Button(window, text="Добавить", command=add_task)
add_button.pack(pady=5)

delete_button = tkinter.Button(window, text="Удалить", command=delete_task)
delete_button.pack(pady=5)

done_button = tkinter.Button(window, text="Выполнено", command=mark_done)
done_button.pack(pady=5)

listbox = tkinter.Listbox(window, width=50, height=15)
listbox.pack(pady=10)


window.after(0, startApp)
window.protocol("WM_DELETE_WINDOW", closeApp)
window.geometry("300x300")

window.mainloop()