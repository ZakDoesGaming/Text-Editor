from tkinter import *
import tkinter.filedialog
import os, sys, inspect
import markdown2
main_path= os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
dependencies_path = os.path.join(main_path, 'dependencies')
sys.path.append(dependencies_path)

class Window():
    def __init__(self, parent):
        self.filename =''
        self.window = Toplevel(parent)
        self.text_box = Text(self.window, background="black", foreground="firebrick", insertbackground="white")
        self.text_box.pack(expand = 1, fill= BOTH)
        self.text_box.focus_set()
       
class Editor:
    def __init__(self, master):
        self.file_name = ""
        self.html_window=""
        #self.html_viewer=""
        
        initial_text_box = Text(root, background="white", foreground="black", insertbackground="white")
        initial_text_box.pack(expand = 1, fill= BOTH)
        initial_text_box.focus_set()
        initial_text_box.insert(END, """Welcome to ZakEdit(Work-In-Progress name) made by Zak Farmer.\nThis program is open-source, do whatever you want.\nI programmed this in Python :)""")

        self.file_opt = options = {}

        # File Options
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt'), ('markdown', '.md'), ('html', '.html')]
        options['initialdir'] = os.path
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'


        # Directory Options
        self.dir_opt = options = {}
        options['initialdir'] = os.path
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'
        
        


        def find_focus():
           focus= root.focus_get()
           print(focus)
           print(focus.get(1.0, END))
           print(focus.master)
           focus.master.wm_title("focused")
           

        menubar = Menu(root)
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_window, accelerator="Command+N")
        filemenu.add_command(label="Open", command=self.open_file, accelerator="Command+O")
        filemenu.add_command(label="Save", command=self.save_file, accelerator="Command+S")
        filemenu.add_command(label="Save as...", command=self.save_as_file)
        filemenu.add_separator()
        filemenu.add_command(label="Close Window", command=self.destroy, accelerator="Command+W")
        filemenu.add_command(label="Exit", command=self.quit_project, accelerator="Command+Q")
        menubar.add_cascade(label="File", menu=filemenu)

                             
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=find_focus)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.cut, accelerator="Command+X")
        editmenu.add_command(label="Copy", command=self.copy, accelerator="Command+C")
        editmenu.add_command(label="Paste", command=self.paste, accelerator="Command+V")
        editmenu.add_command(label="Select All", command=self.select_all, accelerator="Command+A")
        editmenu.add_command(label="Delete", command=self.delete_selection)
        menubar.add_cascade(label="Edit", menu=editmenu)

                             
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)


        root.bind_all("<Command-n>", self.new_window)
        root.bind_all("<Command-o>", self.open_file)
        root.bind_all("<Command-s>", self.save_file)
        root.bind_all("<Command-Shift-s>", self.save_as_file) #This one doesn't work :(
        root.bind_all("<Command-a>", self.select_all)
        root.bind_all("<Command-w>", self.destroy)
        root.bind_all("<Command-q>", self.quit_project)
  
        
    def open_file(self, event=''):
        open_file = tkFileDialog.askopenfile(mode='r', **self.file_opt)
        window_app = Window(root)
        window_app.text_box.delete(1.0, END)
        window_app.text_box.insert(END, open_file.read())
        window_app.file_name = open_file.name
        window_app.window.wm_title(window_app.file_name)
        print(window_app.file_name)

    def save_file(self, event=''):
        focus=root.focus_get()
        if (focus.master.title() == '' or focus.master.title() == "ZakEdit"):
            self.save_as_file()
        else:
             save_file = open(focus.master.wm_title(), 'w')
             save_file.write(focus.get(1.0, END))
    
    def save_as_file(self, event=''):
        focus=root.focus_get()
        save_file = tkFileDialog.asksaveasfile(mode='w', **self.file_opt)
        save_file.write(focus.get(1.0, END))
        focus.master.wm_title(save_file.name)
        print(focus.master.title())

    def copy(self):
        focus=root.focus_get()
        root.clipboard_clear()
        root.clipboard_append(focus.selection_get())

    def cut(self):
        self.copy()
        self.delete_selection()

    def paste(self):
        focus=root.focus_get()
        result = root.selection_get(selection = "CLIPBOARD")
        focus.insert(INSERT, result)

    def delete_selection(self):
        focus=root.focus_get()
        focus.delete(SEL_FIRST, SEL_LAST)
        
    def select_all(self, event=''):
        focus=root.focus_get()
        focus.tag_add("sel","1.0","end")
        
    def new_window(self, event=''):
        self.window_app = Window(root)

    def about(self):
        about_window = Toplevel(root)
        about_window.wm_title("About")
        info = Label(about_window, text="""This is a basic text editor made by Zak Farmer in Python\nIt's programmed in Python using Sublime Text 2 and Python 3.4\nIt's a work in progress and is hardly done yet.\nI'll be releasing versions all the time (Hopefully)\nThanks for using ZakEdit!\n:)""")
        info.pack()
        
    def destroy(self, event=''):
        focus=root.focus_get()
        focus_parent_string=focus.winfo_parent()
        focus_parent = root.nametowidget(focus_parent_string)
        unbind_destroy(focus_parent)
        focus_parent.wm_withdraw()
        try:
            focus_parent.wm_withdraw()
        except: pass
        try:
            focus_parent.destroy()
        except: pass

    def quit_project(self):
        sys.exit()
        
if __name__=='__main__':
    root = Tk()
    root.wm_title("ZakEdit")
    app = Editor(root)
    root.mainloop()
