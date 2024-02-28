import os 
import glob 
import convert 
from pathlib import Path 

import tkinter as tk 
from tkinter import Misc
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk 
# from tkinter import askstring

from PIL import Image, ImageTk

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
        self.total_number_of_images = 0
        
        self.current_image_index = 0 
        self.current_image_bbox_list = [] 
        self.current_image_bbox_objects_ids = [] 
        self.current_class_index = 0
        self.current_rectangle_object = None

        self.x1 = 0
        self.y1 = 0  
        self.x2 = 100
        self.y2 = 100  

        self.point_info = {
            'class':None,
            'point':None
        }

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
    
    def load_image(self):
        self.current_image_path = self.image_list[self.current_image_index]
        self.image = Image.open(self.current_image_path)
        self.center_frame.load_image(self.image)

    def add_class(self):
        new_class = simpledialog.askstring("New Class", "Enter the name of the new class:")
        self.class_list.append(new_class)
        messagebox.showinfo('new class created', f'successfully created new class {new_class}')        

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
        # if self.class_present():
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
        # need to add to the list box to the right frame


    def mouse_right_pressed(self, x, y):
        for object_index, image_bbox_object in enumerate(self.current_image_bbox_objects_ids):
            x1, y1, x2, y2 = self.center_frame.get_coordinates_of_image_canvas_object(image_bbox_object)

            if (x1 <= x <= x2 ) and (y1 <= y <= y2):
                self.center_frame.delete_image_canvas_object(image_bbox_object)
                self.current_image_bbox_objects_ids.pop(object_index)
                self.current_image_bbox_list.pop(object_index)
                # need to delete from right's list box
                

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