import os 
import json
import glob 
import convert 
from pathlib import Path 

import tkinter as tk 
from tkinter import Misc
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk 
# from tkinter import askstring

from PIL import Image, ImageTk

VERSION = '1.0.0'

FILE = Path(__file__).resolve()
BASE_DIR = FILE.parents[0]  

# colors for the bboxes
COLORS = ['red', 'blue', 'olive', 'teal', 'cyan', 'green', 'black', 'purple', 'orange', 'brown','crimson','yellow']

# image sizes for the examples
SIZE = 256, 256
from gui import MenuBar, LeftFrame, CenterFrame, RightFrame, BottomFrame
class LabelTool():
    def __init__(self, master: tk.Tk) -> None:
        self.root = master 
        self.root.title("Yolo Annotator")
        # self.root.resizable(width=tk.TRUE, height=tk.FALSE)
        # self.root.geometry("800x480")

        self.root_frame = tk.Frame(self.root)
        self.root_frame.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.label_tool_variables()

        self.menu_widgets()
        self.bottom_frame_widgets()
        self.left_frame_widgets()
        self.center_frame_widgets()
        self.right_frame_widgets()
        # super().__init__(self.root)

    def menu_widgets(self):
        # menu Bar
        self.menu_bar = MenuBar(master=self.root)
        self.root.config(menu=self.menu_bar)

        self.menu_bar.new_file = self.new_file 


    def label_tool_variables(self):
        self.image_directory = BASE_DIR

        self.image_extensions = ["*.jpg", "*.png"]
        self.image_list = []
        self.class_list = [] 
        self.unique_classes = set([])
        self.total_number_of_images = 0
        
        self.current_image_index = 0 
        self.current_image_bbox_list = [] 
        self.current_image_bbox_objects_ids = [] 
        self.current_rectangle_object = None

        self.x1 = 0
        self.y1 = 0  
        self.x2 = 100
        self.y2 = 100  
        self.current_class_index = 0

        self.shape_info = {
            'label':None,
            'points':[],
            'shape_type': None,
            'group_ids': None, 
        }
        self.file_json_info = {
            'version': VERSION,
            'shapes': [], # self.shape_info
            'image_name': None, 
            'imageHeight': None,
            'imageWidth': None,
        }

        self.bbox_list_str = '{class_name} : ({x1}, {y1}) -> ({x2}, {y2})'

        self.left_mouse_button_pressed = False 
        self.right_mouse_button_pressed = False 

    # methods for menu widgets
    def new_file(self):
        print('is called')
        self.load_image_directory()
        ...

    # methods for left frame widgets
    def left_frame_widgets(self):
        self.left_frame = LeftFrame(self.root_frame, highlightbackground="black", highlightthickness=2)
        self.left_frame.pack(side=tk.LEFT, anchor=tk.N) # grid(row=0, column=0) #anchor=tk.NW)
        
        # assigning the functions 
        self.left_frame.load_image_directory = self.load_image_directory 
        self.left_frame.reset_checkpoint = self.reset_checkpoint
        self.left_frame.next = self.next
        self.left_frame.previous = self.previous 

    # methods for central frame widgets
    def center_frame_widgets(self):
        self.center_frame = CenterFrame(self.root_frame, highlightbackground="black", highlightthickness=2)
        self.center_frame.pack(side=tk.LEFT, anchor=tk.N) # grid(row=0, column=1) 
        
        # assigning the function
        self.center_frame.mouse_left_pressed = self.mouse_left_pressed
        self.center_frame.mouse_left_released = self.mouse_left_released

        self.center_frame.mouse_right_pressed = self.mouse_right_pressed

        self.center_frame.mouse_moved = self.mouse_moved 

    def right_frame_widgets(self):
        self.right_frame = RightFrame(self.root_frame, highlightbackground="red", highlightthickness=2)
        self.right_frame.pack(anchor=tk.E) # grid(row=0, column=1) 
    
        self.right_frame.add_class = self.add_class 
        self.right_frame.combobox_set_class = self.combobox_set_class 

    def bottom_frame_widgets(self):
        # self.bottom_frame = BottomFrame(self.root_frame, highlightbackground="red", highlightthickness=2)
        # self.bottom_frame.pack(side=tk.BOTTOM, anchor=tk.SE, expand=True)
        ...

    # commands methods
    def load_image_directory(self, directory = False):
        print('load image directory')
        if not directory:
            self.root.focus()
            self.image_directory = str(filedialog.askdirectory(initialdir=BASE_DIR, ))
        else:
            assert os.path.exists(directory), "Directory Doesnot exists"
            self.image_directory = directory
        for ext in ('*.png', '*.jpg'):
            self.image_list.extend(glob.glob(os.path.join(self.image_directory, ext)))
        self.total_number_of_images = len(self.image_list)
        if self.total_number_of_images == 0:
            messagebox.showinfo("Error", "No JPG/PNG images found in the specified dir!")
            print('No JPG/PNG images found in the specified dir!')
            return
        self.current_image_index = 0

        self.load_image()
    
    def  load_image(self):
        self.clear_bboxes()
        self.right_frame.clear_bbox_list()
        self.current_image_bbox_objects_ids = []
        self.current_image_bbox_list = [] 

        self.current_image_path = self.image_list[self.current_image_index]
        self.image = Image.open(self.current_image_path)
        self.center_frame.load_image(self.image)
        self.load_bbox_info(self.current_image_path)

    def clear_bboxes(self):
        self.shape_info = {
            'label':None,
            'points':[],
            'shape_type': None,
            'group_ids': None, 
        }
        self.file_json_info = {
            'version': VERSION,
            'shapes': [], # self.shape_info
            'image_name': None, 
            'imageHeight': None,
            'imageWidth': None,
        }
        if len(self.current_image_bbox_objects_ids):
            for image_canvas_object_id in self.current_image_bbox_objects_ids:
                self.center_frame.delete_image_canvas_object(image_canvas_object_id)

    def load_bbox_info(self, current_image_path:str):
        file_extension = current_image_path.split('.')[-1]
        current_json_path = current_image_path.replace('.'+file_extension, '.json')
        if os.path.exists(current_json_path):
           with open(current_json_path, 'r') as current_json_file:
                self.file_json_info = json.load(current_json_file)

                for shape in self.file_json_info['shapes']:
                    if shape['shape_type'] == 'rectangle':
                        current_class = shape['label']
                        if current_class not in self.class_list:
                            self.class_list.append(current_class)
                        self.current_class_index = self.class_list.index(current_class)

                        x1, y1, x2, y2 = shape['points']
                        rectangle_object = self.center_frame.create_rectangle(
                            x1, y1, x2, y2, 
                            width=2, outline=COLORS[self.current_class_index])
                        self.current_image_bbox_objects_ids.append(rectangle_object)
                        self.current_image_bbox_list.append(
                            [self.current_image_index, x1, y1, x2, y2])
                        
                        # adding to the list box to the right frame
                        self.right_frame.insert_to_bbox_list(
                            self.bbox_list_str.format(class_name=self.class_list[self.current_class_index], x1=x1, y1=y1, x2=x2, y2=y2),
                            index=len(self.current_image_bbox_list)-1, 
                            fg=COLORS[self.current_class_index]
                            )
                
                self.right_frame.update_combobox_options(self.class_list, len(self.class_list)-1)
        ...

    def write_bbox_info(self, current_image_path:str):
        file_extension = current_image_path.split('.')[-1]
        current_json_path = current_image_path.replace('.'+file_extension, '.json')
        with open(current_json_path, 'w') as current_json_file:
            json.dump(self.file_json_info, current_json_file)
        ...

    def add_class(self):
        new_class = simpledialog.askstring("New Class", "Enter the name of the new class:")
        if new_class in self.class_list:
            messagebox.showwarning('Class Exists', f'{new_class} already exists')        
            return 
        self.class_list.append(new_class)
        messagebox.showinfo('new class created', f'successfully created new class {new_class}')        
        self.current_class_index = len(self.class_list)-1
        self.right_frame.update_combobox_options(self.class_list, len(self.class_list)-1)

    def combobox_set_class(self):
        selected_class_label = self.right_frame.get_combobox_selected_option()
        if selected_class_label in self.class_list:
            self.current_class_index = self.class_list.index(selected_class_label)
            return 
        messagebox.WARNING('No Class available', f'{selected_class_label} is not available in the class list create it.')
        ...

    def reset_checkpoint(self): 
        # if self.cur == 0 or self.cur==1:
        #     print("Already at the first image. No need to reset.")
        #     # You can display a messagebox or any other appropriate warning mechanism.
        # else:
        #     with open("log/checkpoint.txt", "w") as checkpointFile:
        #         checkpointFile.write("1")
        #     # Load the image associated with the reset checkpoint
        #     self.cur = 1
        #     self.loadImage()
        ...
    
    def next(self):
        self.current_image_index = self.current_image_index + (1 if self.current_image_index< (self.total_number_of_images - 1) else 0) 
        self.load_image()
        ...
    
    def previous(self):
        self.current_image_index = self.current_image_index - (1 if self.current_image_index> 0 else 0) 
        self.load_image()
    
    def class_present(self):
        if not len(self.class_list):
            messagebox.showwarning('No Class', "There is no class to assign, please create a class  ")
            return False
        return True

    def mouse_left_pressed(self, x, y):
        if self.class_present():
            self.left_mouse_button_pressed = True
            self.x1 = x
            self.y1 = y
        ...
    
    def mouse_left_released(self, x, y):
        if self.left_mouse_button_pressed:
            self.left_mouse_button_pressed = False
            self.x2, self.y2 = x, y 
            # self.bbox_id = self.center_frame.image_canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
            #     width=2, outline=COLORS[self.current_class_index])
            if self.current_rectangle_object:
                self.center_frame.delete_image_canvas_object(self.current_rectangle_object)
            
            self.current_rectangle_object = self.center_frame.create_rectangle(
                self.x1, self.y1, self.x2, self.y2, 
                width=2, outline=COLORS[self.current_class_index])
            if self.x1 > self.x2:
                self.x1, self.x2 = self.x2, self.x1 
            if self.y1 > self.y2:
                self.x1, self.x2 = self.x2, self.x1 

            self.current_image_bbox_objects_ids.append(self.current_rectangle_object)
            self.current_image_bbox_list.append([self.current_class_index, self.x1, self.y1, self.x2, self.y2])
            
            self.current_rectangle_object = None

            # adding to the file in json format 
            temp_shape_info = self.shape_info.copy()
            temp_shape_info['label'] = self.class_list[self.current_class_index]
            temp_shape_info['points'] = [self.x1, self.y1, self.x2, self.y2]
            temp_shape_info['shape_type'] = "rectangle"
            self.file_json_info['shapes'].append(temp_shape_info)

            # need to add to the list box to the right frame
            self.right_frame.insert_to_bbox_list(
                self.bbox_list_str.format(class_name=self.class_list[self.current_class_index], x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2),
                index=len(self.current_image_bbox_list)-1, 
                fg=COLORS[self.current_class_index]
                )

            # writing to a json file 
            self.write_bbox_info(self.image_list[self.current_image_index])

    def mouse_right_pressed(self, x, y):
        for object_index, image_bbox_object in enumerate(self.current_image_bbox_objects_ids):
            x1, y1, x2, y2 = self.center_frame.get_coordinates_of_image_canvas_object(image_bbox_object)

            if (x1 <= x <= x2 ) and (y1 <= y <= y2):
                self.center_frame.delete_image_canvas_object(image_bbox_object)
                self.current_image_bbox_objects_ids.pop(object_index)
                self.current_image_bbox_list.pop(object_index)
                self.file_json_info['shapes'].pop(object_index)
                self.write_bbox_info(self.image_list[self.current_image_index])
                # need to delete from right's list box
                self.right_frame.delete_from_bbox_list(object_index)
        ...

    def mouse_moved(self, x, y):
        # if self.left_mouse_button_pressed:
        # self.bbox_id = self.center_frame.image_canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
        #    width=2, outline=COLORS[self.current_class_index])
        if self.left_mouse_button_pressed:
            self.x2, self.y2 = x, y 
            if self.current_rectangle_object:
                self.center_frame.delete_image_canvas_object(self.current_rectangle_object)
            self.current_rectangle_object = self.center_frame.create_rectangle(
                self.x1, self.y1, self.x2, self.y2, 
                width=2, outline=COLORS[self.current_class_index])
        ...

if __name__ == "__main__":
    root = tk.Tk()
    label_tool = LabelTool(root)
    root.mainloop()