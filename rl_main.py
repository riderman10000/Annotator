import os 
import glob 
import convert 
from pathlib import Path 

import tkinter as tk 
from tkinter import Misc
from tkinter import messagebox, filedialog
from tkinter import ttk 
from tkinter.simpledialog import askstring

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
        self.total_number_of_images = 0
        self.current_image_index = 0 

    # methods for menu widgets
    def new_file(self):
        print('is called')
        self.load_image_directory()
        ...

    # methods for left frame widgets
    def left_frame_widgets(self):
        self.left_frame = LeftFrame(self.root_frame, highlightbackground="black", highlightthickness=2)
        self.left_frame.pack(side=tk.LEFT, anchor=tk.N) # grid(row=0, column=0) #anchor=tk.NW)
        self.left_frame.load_image_directory = self.load_image_directory 
        self.left_frame.reset_checkpoint = self.reset_checkpoint
        self.left_frame.next = self.next
        self.left_frame.previous = self.previous 

    # methods for central frame widgets
    def center_frame_widgets(self):
        self.center_frame = CenterFrame(self.root_frame, highlightbackground="black", highlightthickness=2)
        self.center_frame.pack(side=tk.LEFT, anchor=tk.N) # grid(row=0, column=1) 

    def right_frame_widgets(self):
        self.right_frame = RightFrame(self.root_frame, highlightbackground="red", highlightthickness=2)
        self.right_frame.pack(anchor=tk.E) # grid(row=0, column=1) 
    
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

if __name__ == "__main__":
    root = tk.Tk()
    label_tool = LabelTool(root)
    root.mainloop()