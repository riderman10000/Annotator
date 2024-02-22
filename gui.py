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

class LeftFrame(tk.Frame):
    @inherit_signature_from(tk.Frame.__init__)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


        self.load_directory_button = tk.Button(self.master, text="Open Image Directory", bg='#84a59d',relief='flat',command = self.load_directory_button_command)
        self.load_image_directory = None  # assgin the actual statment to this variable

        self.reset_checkpoint_button = tk.Button(self.master, text='Reset Checkpoint',bg='#C9ADA7',relief='flat', command = self.reset_checkpoint_command)
        self.reset_checkpoint = None # assgin the actual statment to this variable

        self.load_checkpoint_button = tk.Button(self.master, text='Load Checkpoint',bg='#C9ADA7',relief='flat', command = self.load_checkpoint_command) 
        self.load_checkpoint = None # assgin the actual statment to this variable
        
        self.previous_button = tk.Button(self.master, text='<< Prev', width = 10,bg='#669BBC',relief='flat', command = self.previous_command)
        self.previous = None # assgin the actual statment to this variable

        self.skip_button = tk.Button(self.master, text ='Skip', width = 10,bg='#f28482',relief='flat', command = self.skip_command)
        self.skip = None # assgin the actual statment to this variable

        self.next_button = tk.Button(self.master, text='Next >>', width = 10,bg='#669BBC',relief='flat', command = self.next_command)
        self.next = None # assgin the actual statment to this variable

        self.place_widgets()

    def place_widgets(self):
        self.load_directory_button.grid(row=0, column=0, sticky=tk.W + tk.E, padx=5, pady=1)
        self.reset_checkpoint_button.grid(row=1, column=0, sticky=tk.W + tk.E, padx=5, pady=1)
        self.load_checkpoint_button.grid(row=2, column=0, sticky=tk.W + tk.E, padx=5, pady=1)
        self.previous_button.grid(row=3 , column=0, sticky=tk.W + tk.E, padx = 5, pady = 1)
        self.skip_button.grid(row=4 , column=0, sticky=tk.W + tk.E, padx = 5, pady = 1)
        self.next_button.grid(row=5 , column=0, sticky=tk.W + tk.E, padx = 5, pady = 1)        

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

class MenuBar(tk.Menu):
    # @inherit_signature_from(tk.Menu)
    @inherit_signature_from(tk.Menu.__init__)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.file_menu = tk.Menu(self, tearoff=False)
        
        self.make_menu()
        self.set_commands()
        self.set_shortcuts()

    def make_menu(self):
        self.add_cascade(menu=self.file_menu, label="File")
    
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
    
    def set_commands(self):
        self.file_menu.add_command(
            label="New",
            accelerator="Ctrl+N",
            command=self.command_new_file
        )
        self.new_file = None 
    
    def set_shortcuts(self):
        self.master.bind_all('<Control-n>', self.command_new_file)
        self.master.bind_all('<Control-N>', self.command_new_file)

    @button_method_assign_warning('new_file')
    def command_new_file(self, event=None):
        self.new_file()
        ...

if __name__ == "__main__":
    root = tk.Tk() 
    menu_bar = MenuBar(master=root)
    root.config(menu=menu_bar)
    left_frame = LeftFrame(root)
    left_frame.message = 'test'
    print(left_frame.message, LeftFrame.message)
    root.mainloop()
