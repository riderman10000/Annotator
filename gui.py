# from _tkinter import Tcl_Obj
# from tkinter import Misc
from typing import Callable, Any, TypeVar, Optional
from typing_extensions import ParamSpec

import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

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

share_info = {
    'x':0,
    'y':0,
}

class shared_data:
    x = 0
    y = 0

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
        def decorator(function):
            def wrapper(*args, **kwargs):                
                try:
                    function(*args, **kwargs)
                except Exception as e:
                    print(f'assign your method to Left Frame Variable Name: {function_name}', e)
            return wrapper
        return decorator

    @button_method_assign_warning('load_image_directory')
    def load_directory_button_command(self):
        self.load_image_directory()
        ...

    @button_method_assign_warning('reset_checkpoint')
    def reset_checkpoint_command(self):
        self.reset_checkpoint()

    @button_method_assign_warning('load_checkpoint')
    def load_checkpoint_command(self):
        self.load_checkpoint()
    
    @button_method_assign_warning('previous')
    def previous_command(self, event = None):
        self.previous()
        
    @button_method_assign_warning('skip')
    def skip_command(self):
        self.skip()
    
    @button_method_assign_warning('next')
    def next_command(self, event = None):
        self.next()    


class BottomFrame(tk.Frame):
    @inherit_signature_from(tk.Frame.__init__)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        try :
            master = self.master.master
        except Exception as e :
            master = self 

        self.go_entry = tk.Button(master, text = 'Go',bg='#dde5b6',relief='ridge') # , command = self.gotoImage)
        self.go_to_image_label = tk.Label(master, text = "Go to Image No.")
        self.image_number_entry = tk.Entry(master, width = 5)
        self.progress_label = tk.Label(master, text = "Progress:     /    ")
        self.mouse_position_label = tk.Label(master, text='x: 0, y: 0')        

        self.place_widgets()

    def place_widgets(self):
        self.mouse_position_label.pack(side=tk.RIGHT)
        self.go_entry.pack(side=tk.RIGHT)
        self.image_number_entry.pack(side=tk.RIGHT)
        self.go_to_image_label.pack(side=tk.RIGHT)
        self.progress_label.pack(side=tk.RIGHT)
        ...

class CenterFrame(BottomFrame):
    @inherit_signature_from(tk.Frame.__init__)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.widgetName = "CenterFrame"
        self.horizontal_bar = tk.Scrollbar(self, orient='horizontal')
        self.vertical_bar = tk.Scrollbar(self, orient='vertical')

        self.width = 2000
        self.height = 2000

        self.image = Image.new('RGB', (self.width, self.height), color=(0, 255, 0))
        self.tk_canvas_image = ImageTk.PhotoImage(self.image)

        self.image_canvas = tk.Canvas(self, cursor='tcross', width=1000, height=630,
            scrollregion=(0, 0 , self.tk_canvas_image.width(), self.tk_canvas_image.height()),
            xscrollcommand=self.horizontal_bar.set, yscrollcommand=self.vertical_bar.set,
            highlightbackground="black", highlightthickness=2)
        self.image_canvas.widgetName = "image_canvas"

        self.horizontal_bar.config(command=self.image_canvas.xview)
        self.vertical_bar.config(command=self.image_canvas.yview)

        self.left = None 
        self.right = None 
        self.up = None 
        self.down = None 

        self.mouse_left_pressed = None 
        self.mouse_left_released = None 

        self.mouse_right_pressed = None 
        self.mouse_right_released = None 
        
        self.mouse_moved = None 

        self.mouse_events = {
            'left_button_down': False,
            'left_button_up': False,
            'right_button_down': False,
            'right_button_up': False,
        }

        self.place_widgets_center()
        self.set_shortcuts()

    def place_widgets_center(self):
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
        self.image_canvas.bind_all('<ButtonPress-1>', self.mouse_left_pressed_command)
        self.image_canvas.bind_all('<ButtonRelease-1>', self.mouse_left_released_command)
        
        self.image_canvas.bind_all('<ButtonPress-3>', self.mouse_right_pressed_command)
        self.image_canvas.bind_all('<ButtonRelease-3>', self.mouse_right_released_command)
        
        self.image_canvas.bind_all('<Motion>', self.mouse_moved_command)

    def button_method_assign_warning(function_name):
        def decorator(function):
            def wrapper(*args, **kwargs):
                try:
                    function(*args, **kwargs)
                except Exception as e:
                    print(f'assign your method to Central Frame Variable Name: {function_name}, error: {e}')
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

    @button_method_assign_warning('mouse_left_pressed')
    def mouse_left_pressed_command(self, event):
        widget_name = 'image_canvas'
        if event.widget.widgetName == widget_name: # will track this frame's mouse movement only
            print(f'{event}')
            x = self.image_canvas.canvasx(event.x)
            y = self.image_canvas.canvasy(event.y)
            self.mouse_left_pressed(x, y)

    @button_method_assign_warning('mouse_left_released')
    def mouse_left_released_command(self, event):
        widget_name = 'image_canvas'
        if event.widget.widgetName == widget_name: # will track this frame's mouse movement only
            print(f'{event}')
            x = self.image_canvas.canvasx(event.x)
            y = self.image_canvas.canvasy(event.y)
            self.mouse_left_released(x, y)
    
    @button_method_assign_warning('mouse_right_pressed')
    def mouse_right_pressed_command(self, event):
        widget_name = 'image_canvas'
        if event.widget.widgetName == widget_name: # will track this frame's mouse movement only
            print(f'{event}')
            x = self.image_canvas.canvasx(event.x)
            y = self.image_canvas.canvasy(event.y)
            self.mouse_right_pressed(x, y)

    @button_method_assign_warning('mouse_right_released')
    def mouse_right_released_command(self, event):
        widget_name = 'image_canvas'
        if event.widget.widgetName == widget_name: # will track this frame's mouse movement only
            print(f'{event}')
            x = self.image_canvas.canvasx(event.x)
            y = self.image_canvas.canvasy(event.y)
            self.mouse_right_released(x, y)

    @button_method_assign_warning('mouse_moved')
    def mouse_moved_command(self, event: tk.Event):
        widget_name = 'image_canvas'
        if event.widget.widgetName == widget_name: # will track this frame's mouse movement only
            x = self.image_canvas.canvasx(event.x)
            y = self.image_canvas.canvasy(event.y)
            overlapping = self.image_canvas.find_overlapping(x, y, x+1, y+1)
            print('overlaaping', overlapping)
            self.mouse_position_label.config(text=f'x: {x}, y: {y}')
            self.mouse_moved(x, y)
        
    def load_image(self, image: Image = None):
        if type(None) == type(image):
            self.image = Image.new('RGB', (self.width, self.height))
        else:
            self.image = image
        
        self.tk_canvas_image = ImageTk.PhotoImage(self.image)
        self.image_canvas.config(
            scrollregion=(0, 0, self.tk_canvas_image.width(), self.tk_canvas_image.height())
        )
        self.image_canvas.create_image(0, 0, image=self.tk_canvas_image, anchor=tk.NW)

        # self.progress_label.config(text=f'')
    def create_rectangle(self, x1, y1, x2, y2, width = 1, outline='red'):
        rectangle_id = self.image_canvas.create_rectangle(x1, y1, x2, y2, width=width, outline=outline)
        return rectangle_id
    
    def delete_image_canvas_object(self, image_canvas_object_id):
        self.image_canvas.delete(image_canvas_object_id)
    
    def get_coordinates_of_image_canvas_object(self, image_canvas_object_id):
        return self.image_canvas.coords(image_canvas_object_id)



class RightFrame(tk.Frame):
    @inherit_signature_from(tk.Frame.__init__)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.class_name = tk.StringVar()
        self.current_class_label = tk.Label(self, text='Select Object Class')
        self.current_class_combobox = ttk.Combobox(self, state='readonly', textvariable=self.class_name)
        self.combobox_set_class = None 
        self.num_keys = None 
        
        self.add_class_button = tk.Button(self, text='Add Class', bg='#4cc9f0',fg = 'white',relief='raised',command=self.add_class_command)
        self.add_class = None 

        self.delete_class_button = tk.Button(self, text='Delete Class', bg='#f28482',fg = 'white',relief='raised',command=self.delete_class_command)
        self.delete_class = None 

        self.bbox_list_frame = tk.Frame(self)
        self.bbox_list_frame_label = tk.Label(self.bbox_list_frame, text='Bounding Box List')
        self.bbox_list_box = tk.Listbox(self.bbox_list_frame, width=40, height=12)
        
        self.clear_bbox_button = tk.Button(self, text = 'Clear', bg='#c1121f',fg = 'white',relief='groove',command = self.clear_bbox_command)
        self.clear_bbox = None 
        
        self.clear_all_bbox_button = tk.Button(self, text = 'ClearAll',bg='#c1121f',fg = 'white',relief='groove', command = self.clear_all_bbox_command)
        self.clear_all_bbox = None 

        self.file_list_frame = tk.Frame(self)
        self.file_list_frame_label = tk.Label(self.file_list_frame, text='File List')
        self.file_list_list_box = tk.Listbox(self.file_list_frame, width=40, height=12)

        self.place_widgets()
        self.set_shortcuts() 

    def place_widgets(self):
        self.current_class_label.grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.E)
        self.current_class_combobox.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)
        self.add_class_button.grid(row=2, column=0, sticky=tk.W + tk.E)
        self.delete_class_button.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.bbox_list_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)
        self.bbox_list_frame_label.grid(row=0, column=0)
        self.bbox_list_box.grid(row=1, column=0)

        self.clear_bbox_button.grid(row=7, column=0, columnspan=2, sticky=tk.W + tk.E)
        self.clear_all_bbox_button.grid(row=7, column=0,columnspan=2, sticky=tk.E + tk.W)
        
        self.file_list_frame.grid(row=9, column=0, columnspan=2, sticky=tk.W + tk.E)
        self.file_list_frame_label.grid(row=0, column=0)
        self.file_list_list_box.grid(row=1, column=0)

        # self.file_list_list_box.grid(row=8, column=0, columnspan=2, sticky=tk.W + tk.E)
        ...
    
    def set_shortcuts(self):
        self.bind('<Key>', self.num_keys_command)
        self.current_class_combobox.bind('<<ComboboxSelected>>', self.combobox_set_class_command)
        ...

    def button_method_assign_warning(function_name):
        def decorator(function):
            def wrapper(*args, **kwargs):
                try:
                    function(*args, **kwargs)
                except Exception as e:
                    print(f'assign your method to Right Frame Variable Name: {function_name}', e)
            return wrapper
        return decorator
    
    @button_method_assign_warning('add_class')
    def add_class_command(self, event=None):
        print(f'{event}')
        self.add_class()

    @button_method_assign_warning('delete_class')
    def delete_class_command(self, event):
        print(f'{event}')
        self.delete_class()

    @button_method_assign_warning('clear_bbox')
    def clear_bbox_command(self):
        self.clear_bbox()

    @button_method_assign_warning('clear_all_bbox')
    def clear_all_bbox_command(self):
        self.clear_all_bbox()
    
    @button_method_assign_warning('combobox_set_class')
    def combobox_set_class_command(self, event: tk.Event):
        self.combobox_set_class()
    
    @button_method_assign_warning('num_keys')
    def num_keys_command(self, event: tk.Event):
        if event.char.isdigit():
            digit = int(event.char) -1 
            self.num_keys(digit)

    def get_combobox_selected_option(self):
        return self.current_class_combobox.get()

    def update_combobox_options(self, options, class_index=0):
        self.current_class_combobox['values'] = options
        self.current_class_combobox.current(class_index)

        ...



if __name__ == "__main__":
    root = tk.Tk() 
    menu_bar = MenuBar(master=root)
    root.config(menu=menu_bar)
    left_frame = LeftFrame(root)
    root.mainloop()