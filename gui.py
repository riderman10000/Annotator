from _tkinter import Tcl_Obj
from tkinter import Misc
from typing import Callable, Any, TypeVar, Optional
from typing_extensions import ParamSpec

import tkinter as tk

P = ParamSpec('P')
T = TypeVar('T')

def catch_exception(function: Callable[P, T]) -> Callable[P, Optional[T]]:
    def decorator(*args: P.args, **kwargs: P.kwargs)-> Optional[T]:
        try:
            return function(*args, **kwargs)
        except Exception:
            return None
    return decorator

def inherit_signature_from(
        _to:Callable[P, T]
        ) -> Callable[[Callable[..., T]], Callable[P, T]]:
    """
    set the signature checked by pyright/vscode to the signature of another funciton.
    """
    return lambda x: x # type: ignore

class MenuBar(tk.Menu):
    @inherit_signature_from(tk.Menu.__init__)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.file_menu = tk.Menu(self, tearoff=False)
        self.tools_menu = tk.Menu(self, tearoff=False)
        # self.export_yolo_menu = tk.Menubutton(self.tools_menu)

        self.make_menu()
        self.set_option_commands()
        self.set_shortcuts()

    def make_menu(self):
        self.add_cascade(menu=self.file_menu, label="File")
        self.add_cascade(menu=self.tools_menu, label="Tools")
        # self.tools_menu.add_cascade(menu=self.export_yolo_menu, label="Export Yolo")

    def button_method_assign_warning(function_name):
        print('in button method')
        def decorator(function):
            def wrapper(*args, **kwargs):
                try:
                    function(*args, **kwargs)
                except Exception as e:
                    print(f'assign your method to Menu Bar Variable Name: {function_name}')
            return wrapper
        return decorator
    ...
    
    def set_option_commands(self):
        self.file_menu.add_command(
            label="New",
            accelerator="Ctrl+N",
            command=self.new_file_command
        )
        self.new_file = None 

        self.tools_menu.add_command(
            label="Export Yolo",
            accelerator="Y",
            command=self.export_yolo_command
        )
        self.export_yolo = None 

    def set_shortcuts(self):
        self.master.bind_all('<Control-n>', self.new_file_command)
        self.master.bind_all('<Control-N>', self.new_file_command)

    # file options commands 
    @button_method_assign_warning('new_file')
    def new_file_command(self, event=None):
        self.new_file()

    # tools options commands
    @button_method_assign_warning('export_yolo')
    def export_yolo_command(self, event=None):
        self.export_yolo()

class LeftFrame(tk.Frame):
    @inherit_signature_from(tk.Frame.__init__)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


        self.load_directory_button = tk.Button(self, text="Open Image Directory", bg='#84a59d',relief='flat',command = self.load_directory_button_command)
        self.load_image_directory = None  # assgin the actual statment to this variable

        self.reset_checkpoint_button = tk.Button(self, text='Reset Checkpoint',bg='#C9ADA7',relief='flat', command = self.reset_checkpoint_command)
        self.reset_checkpoint = None # assgin the actual statment to this variable

        self.load_checkpoint_button = tk.Button(self, text='Load Checkpoint',bg='#C9ADA7',relief='flat', command = self.load_checkpoint_command) 
        self.load_checkpoint = None # assgin the actual statment to this variable
        
        self.previous_button = tk.Button(self, text='<< Prev', width = 10,bg='#669BBC',relief='flat', command = self.previous_command)
        self.previous = None # assgin the actual statment to this variable

        self.skip_button = tk.Button(self, text ='Skip', width = 10,bg='#f28482',relief='flat', command = self.skip_command)
        self.skip = None # assgin the actual statment to this variable

        self.next_button = tk.Button(self, text='Next >>', width = 10,bg='#669BBC',relief='flat', command = self.next_command)
        self.next = None # assgin the actual statment to this variable

        self.place_widgets()
        self.set_shortcuts()

    def place_widgets(self):
        self.load_directory_button.grid(row=0, column=0, sticky=tk.W + tk.E, padx=5, pady=1)
        self.reset_checkpoint_button.grid(row=1, column=0, sticky=tk.W + tk.E, padx=5, pady=1)
        self.load_checkpoint_button.grid(row=2, column=0, sticky=tk.W + tk.E, padx=5, pady=1)
        self.previous_button.grid(row=3 , column=0, sticky=tk.W + tk.E, padx = 5, pady = 1)
        self.skip_button.grid(row=4 , column=0, sticky=tk.W + tk.E, padx = 5, pady = 1)
        self.next_button.grid(row=5 , column=0, sticky=tk.W + tk.E, padx = 5, pady = 1)        

    def set_shortcuts(self):
        self.master.bind_all('d', self.next_command)
        self.master.bind_all('s', self.skip_command)
        self.master.bind_all('a', self.previous_command)

    def button_method_assign_warning(function_name):
        print('in button method')
        def decorator(function):
            def wrapper(*args, **kwargs):
                try:
                    function(*args, **kwargs)
                except Exception as e:
                    print(f'assign your method to Left Frame Variable Name: {function_name}')
            return wrapper
        return decorator

    @button_method_assign_warning('load_image_directory')
    def load_directory_button_command(self, file_name: str = "chhabi"):
        self.load_image_directory()
        ...

    @button_method_assign_warning('reset_checkpoint')
    def reset_checkpoint_command(self):
        self.reset_checkpoint()

    @button_method_assign_warning('load_checkpoint')
    def load_checkpoint_command(self):
        self.load_checkpoint()
    
    @button_method_assign_warning('previous')
    def previous_command(self):
        self.previous()
        
    @button_method_assign_warning('skip')
    def skip_command(self):
        self.skip()
    
    @button_method_assign_warning('next')
    def next_command(self):
        self.next()    


class CenterFrame(tk.Frame):
    @inherit_signature_from(tk.Frame.__init__)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.horizontal_bar = tk.Scrollbar(self, orient='horizontal')
        self.vertical_bar = tk.Scrollbar(self, orient='vertical')

        self.image_canvas = tk.Canvas(self, cursor='tcross', width=800, height=630,
            scrollregion=(0, 0 , 2000, 2000),
            xscrollcommand=self.horizontal_bar.set, yscrollcommand=self.vertical_bar.set,
            highlightbackground="black", highlightthickness=2)

        self.left = None 
        self.right = None 
        self.up = None 
        self.down = None 

        self.load_image = None 

        self.mouse_right_click = None 
        self.mouse_left_click = None 
        self.mouse_moved = None 

        self.place_widgets()
        self.set_shortcuts()

    def place_widgets(self):
        self.vertical_bar.pack(side=tk.RIGHT, anchor=tk.NE, fill=tk.Y, expand=tk.TRUE)
        self.horizontal_bar.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.X)
        self.image_canvas.pack(side=tk.TOP, anchor=tk.NW, expand=tk.YES, fill=tk.BOTH)

    def set_shortcuts(self):
        # keys 
        self.image_canvas.bind_all('<Left>', self.left_command)
        self.image_canvas.bind_all('<Right>', self.right_command)
        self.image_canvas.bind_all('<Up>', self.up_command)
        self.image_canvas.bind_all('<Down>', self.down_command)
        
        # mouse 
        self.image_canvas.bind_all('<Button-1>', self.mouse_left_click_command)
        self.image_canvas.bind_all('<Button-3>', self.mouse_right_click_command)
        self.image_canvas.bind_all('<Motion>', self.mouse_moved_command)

    def button_method_assign_warning(function_name):
        print('in button method')
        def decorator(function):
            def wrapper(*args, **kwargs):
                try:
                    function(*args, **kwargs)
                except Exception as e:
                    print(f'assign your method to Central Frame Variable Name: {function_name}')
            return wrapper
        return decorator
    
    @button_method_assign_warning('up')
    def up_command(self):
        self.up()
    
    @button_method_assign_warning('down')
    def down_command(self):
        self.down()
    
    @button_method_assign_warning('left')
    def left_command(self):
        self.left()
    
    @button_method_assign_warning('right')
    def right_command(self):
        self.right()

    @button_method_assign_warning('load_image')
    def load_image_command(self):
        self.load_image()

    @button_method_assign_warning('mouse_left_click')
    def mouse_left_click_command(self):
        self.mouse_left_click()

    @button_method_assign_warning('mouse_right_click')
    def mouse_right_click_command(self):
        self.mouse_right_click()

    @button_method_assign_warning('mouse_moved')
    def mouse_moved_command(self, event):
        x = self.image_canvas.canvasx(event.x)
        y = self.image_canvas.canvasy(event.y)
        print(f'event : x - {x}, y - {y}')
        self.mouse_moved(x, y)
    
    

if __name__ == "__main__":
    root = tk.Tk() 
    menu_bar = MenuBar(master=root)
    root.config(menu=menu_bar)
    left_frame = LeftFrame(root)
    root.mainloop()