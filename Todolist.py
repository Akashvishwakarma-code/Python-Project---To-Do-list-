ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp:
    def __init__(self):
        self.root=ctk.CTk()
        self.root.title("Simple todo list app")
        self.root.geometry("400x400+900+250")
        self.root.resizable(False,False)
        self.root.attributes("-topmost",False)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-alpha", 0.9) 
        self.init_database()
        self.setup_ui()
        self.load_task()
        self.root.mainloop()


    def init_database(self):
        self.conn=sqlite3.connect("tod.db")
        self.cur=self.conn.cursor()

        self.cur.execute(""" 
            CREATE TABLE IF NOT EXISTS todo(
                id INTEGER PRIMARY KEY AUTOINCREMENT  ,
                task TEXT NOT NULL,
                completed INTEGER DEFAULT 0)""")
        self.conn.commit()

    def setup_ui(self):
        self.lbl=ctk.CTkLabel(self.root,text="To-do App",font=ctk.CTkFont(size=20,weight="bold"))
        self.lbl.pack(padx=10,pady=20,fill="x")

        #input_frame
        self.input_frame=ctk.CTkFrame(self.root)
        self.input_frame.pack(pady=10,padx=10,fill="x")

        self.input=ctk.CTkEntry(self.input_frame,placeholder_text="Enter task here ...",font=ctk.CTkFont(size=15,weight="bold"))
        self.input.pack(side="left",pady=10,padx=5,expand=True,fill="x")
        self.input.bind("<Return>",lambda e: self.add_text())

        self.btn=ctk.CTkButton(self.input_frame,text="Add",corner_radius=20,command=self.add_text)
        self.btn.pack(side="right",pady=10,padx=10,fill="x")

        self.tasks_frame=ctk.CTkScrollableFrame(self.root,corner_radius=20)
        self.tasks_frame.pack(pady=10,padx=10,expand=True,fill="x")



    def add_text(self):
        task_text=self.input.get().strip()

        if task_text:
            try:
                self.cur.execute("INSERT INTO todo(task) VALUES (?)",(task_text,))
                self.conn.commit()

                self.input.delete(0,"end")

            except Exception as e:
                messagebox.showerror("Error","Something went wrong on serverside")
        else:
            messagebox.showwarning("Empty Field","Enter the tasks!")

        self.load_task()


    def load_task(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        self.cur.execute("SELECT * FROM todo ORDER BY id ASC")
        tasks=self.cur.fetchall()


        for task in tasks:
            task_id,task_text,completed=task

            self.task_frame=ctk.CTkFrame(self.tasks_frame)
            self.task_frame.pack(pady=5,fill="x")

            var=ctk.IntVar(value=completed)
            checkbox=ctk.CTkCheckBox(self.task_frame,text="",variable=var,command=lambda id=task_id,v=var: self.toggle_task(id,v.get()))
            checkbox.pack(side="left",padx=10)

            text=ctk.CTkLabel(self.task_frame,text=task_text)
            text.pack(padx=2,side="left",expand=True,fill="x")

            del_btn=ctk.CTkButton(self.task_frame,text="Delete",width=60,command=lambda id=task_id:self.delete_task(id))
            del_btn.pack(padx=5,side="right")

    def toggle_task(self,task_id,completed):
        self.cur.execute("UPDATE todo SET completed=? WHERE id=?",(completed,task_id,))
        self.conn.commit()
        self.load_task()

    def delete_task(self,task_id):
        self.cur.execute("DELETE FROM todo WHERE id=? ",(task_id,))
        self.conn.commit()
        self.load_task()


















if __name__=="__main__":
    MainApp()











































# import sqlite3

# # Set appearance
# ctk.set_appearance_mode("Dark")
# ctk.set_default_color_theme("blue")

# class SimpleTodoApp:
#     def __init__(self):
#         self.root = ctk.CTk()
#         self.root.title("Simple Todo List")
#         self.root.geometry("500x400")
        
#         # Setup database
#         self.setup_database()
        
#         # Create UI
#         self.create_widgets()
        
#         # Load tasks
#         self.load_tasks()
        
#     def setup_database(self):
#         """Setup SQLite database"""
#         self.conn = sqlite3.connect('todo.db')
#         self.cursor = self.conn.cursor()
        
#         # Create table if it doesn't exist
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS tasks (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 task TEXT NOT NULL,
#                 completed INTEGER DEFAULT 0
#             )
#         ''')
#         self.conn.commit()
        
#     def create_widgets(self):
#         """Create the UI widgets"""
#         # Title
#         self.title = ctk.CTkLabel(self.root, text="My Todo List", 
#                                  font=ctk.CTkFont(size=20, weight="bold"))
#         self.title.pack(pady=10)
        
#         # Input frame
#         self.input_frame = ctk.CTkFrame(self.root)
#         self.input_frame.pack(pady=10, padx=20, fill="x")
        
#         self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter a new task...")
#         self.task_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)
#         self.task_entry.bind("<Return>", lambda e: self.add_task())
        
#         self.add_btn = ctk.CTkButton(self.input_frame, text="Add", command=self.add_task)
#         self.add_btn.pack(side="right", padx=10, pady=10)
        
#         # Tasks frame (scrollable)
#         self.tasks_frame = ctk.CTkScrollableFrame(self.root)
#         self.tasks_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
#     def add_task(self):
#         """Add a new task to the list and database"""
#         task_text = self.task_entry.get().strip()
#         if task_text:
#             # Add to database
#             self.cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task_text,))
#             self.conn.commit()
            
#             # Clear entry
#             self.task_entry.delete(0, "end")
            
#             # Reload tasks
#             self.load_tasks()
        
#     def load_tasks(self):
#         """Load tasks from database and display them"""
#         # Clear current tasks
#         for widget in self.tasks_frame.winfo_children():
#             widget.destroy()
            
#         # Get tasks from database
#         self.cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
#         tasks = self.cursor.fetchall()
        
#         # Display tasks
#         for task in tasks:
#             task_id, task_text, completed = task
            
#             # Task frame
#             task_frame = ctk.CTkFrame(self.tasks_frame)
#             task_frame.pack(fill="x", pady=5)
            
#             # Checkbox
#             var = ctk.IntVar(value=completed)
#             checkbox = ctk.CTkCheckBox(task_frame, text="", variable=var,
#                                       command=lambda id=task_id, v=var: self.toggle_task(id, v.get()))
#             checkbox.pack(side="left", padx=10)
            
#             # Task label
#             label = ctk.CTkLabel(task_frame, text=task_text, 
#                                 font=ctk.CTkFont(size=14, 
#                                                 overstrike=True if completed else False))
#             label.pack(side="left", padx=10, fill="x", expand=True)
            
#             # Delete button
#             delete_btn = ctk.CTkButton(task_frame, text="Delete", width=60,
#                                       command=lambda id=task_id: self.delete_task(id))
#             delete_btn.pack(side="right", padx=5)
            
#     def toggle_task(self, task_id, completed):
#         """Toggle task completion status"""
#         self.cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", 
#                            (completed, task_id))
#         self.conn.commit()
#         self.load_tasks()  # Refresh the list
        
#     def delete_task(self, task_id):
#         """Delete a task"""
#         self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
#         self.conn.commit()
#         self.load_tasks()  # Refresh the list
        
#     def run(self):
#         """Run the application"""
#         self.root.mainloop()
        
#     def __del__(self):
#         """Cleanup when app closes"""
#         if hasattr(self, 'conn'):
#             self.conn.close()

# # Create and run the app
# if __name__ == "__main__":
#     app = SimpleTodoApp()
#     app.run()
