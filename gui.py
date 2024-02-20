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

        self.load_directory_button = tk.Button(self, text="Open Image Directory", bg='#84a59d',relief='flat',command = self.load_directory_button_command)
        self.load_image_directory = None 

        # self.reset_checkpoint_button = tk.Button(self, text='ResetCheckpoint',bg='#C9ADA7',relief='flat', width = 15, command = self.reset_checkpoint_command)
        self.reset_checkpoint = None 

        self.place_widgets()

    def place_widgets(self):
        self.load_directory_button.grid(row=0, column=0, sticky=tk.W + tk.E, padx=5)

    def load_directory_button_command(self, directory=None):
        """
        define your logic to load image directory
        """
        if self.load_image_directory:
            self.load_image_directory()
            return 
        print('Left frame button condition not given')
        ...

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
        ...
    
    def set_commands(self):
        self.file_menu.add_command(
            label="New",
            accelerator="Ctrl+N",
            command=self.command_new_file
        )
    
    def set_shortcuts(self):
        self.master.bind_all('<Control-n>', self.command_new_file)
        self.master.bind_all('<Control-N>', self.command_new_file)

    def command_new_file(self, event=None):
        print('New file open')
        print(event)

        ...

if __name__ == "__main__":
    root = tk.Tk() 
    menu_bar = MenuBar(master=root)
    root.config(menu=menu_bar)
    left_frame = LeftFrame(root)
    root.mainloop()