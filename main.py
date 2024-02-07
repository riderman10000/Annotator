from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter
from tkinter.simpledialog import askstring


import os
import glob
import convert

from PIL import *

# colors for the bboxes
COLORS = ['red', 'blue', 'olive', 'teal', 'cyan', 'green', 'black', 'purple', 'orange', 'brown']

# image sizes for the examples
SIZE = 256, 256

class LabelTool():
    def __init__(self, master, initial_image_dir = None ):
        # set up the main frame
        self.parent = master
        self.initial_image_dir = initial_image_dir if (initial_image_dir) else os.getcwd()
        self.parent.title("Yolo Annotator")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=True)
        self.parent.resizable(width = FALSE, height = FALSE)

        #color picker
        self.index = 0

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.xmlOutDir =''
        self.cur = 0
        self.total = 0
        self.category = ''
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None
        self.currentLabelclass = ''
        self.cla_can_temp = []
        self.classcandidate_filename = 'class.txt'
        self.classcnt = 0

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.hl = None
        self.vl = None
        self.selected_bbox = None
        self.bbox_cnt = 0

        self.class_to_color = {}
        self.class_list_from_file = {'color':[]} #store class list from file



        # ----------------- GUI stuff ---------------------

        self.ldProjBtn = Button(self.frame, text = "Load Image", command = self.loadDir)
        self.ldProjBtn.grid(row = 0, column = 0,sticky = W+E, padx=5)

        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Button-3>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.mainPanel.bind('v', self.pasteLastBbox) #press 'v' to get bbox of last drawn
        self.parent.bind("a", self.prevImage) # press 'a' to go backforward
        self.parent.bind("d", self.nextImage) # press 'd' to go forward
        self.parent.bind("r", self.clearBBoxShortcut)

        self.mainPanel.grid(row = 1, column = 1, columnspan = 3, rowspan = 4, sticky = W+N)

		# Add two buttons for adding and deleting classes in the same row
        self.btnAddClass = Button(self.frame, text='Add Class', command=self.addNewClass)
        self.btnAddClass.grid(row=2, column=4, sticky=W+E, padx=(50, 130))

        self.btnDeleteClass = Button(self.frame, text='Delete Class', command=self.deleteClass)
        self.btnDeleteClass.grid(row=2, column=4, sticky=W+E, padx=(150, 50))

        # choose class
        self.classname = StringVar()
        self.classcandidate = ttk.Combobox(self.frame, state='readonly', textvariable=self.classname)
        self.classcandidate.grid(row=1, column=4)

        if os.path.exists(self.classcandidate_filename):
            with open(self.classcandidate_filename) as cf:
                for line in cf.readlines():
                    self.cla_can_temp.append(line.strip('\n'))
                    self.classcnt += 1

            if self.cla_can_temp:
                self.classcandidate['values'] = self.cla_can_temp
                # print(self.classcandidate.current(0))
                self.classcandidate.current(0)
                self.parent.bind('<Key>', self.setClassShortcut)
                self.currentLabelclass = self.classcandidate.get()  # init
                self.classcandidate.bind('<<ComboboxSelected>>', self.setClass)
            else:
                # Handle case where class list is empty
                self.classcandidate.set("No classes available")
                self.classcandidate['values'] = ["No classes available"]
        else:
            # Handle case where class candidate file does not exist
            self.classcandidate.set("Class file not found")
            self.classcandidate['values'] = ["Class file not found"]

        

		# Add a label for total bounding boxes
        self.totalBboxLabel = Label(self.frame, text='Total BBoxes: 0')
        self.totalBboxLabel.grid(row=3, column=4,sticky=W+E, padx=(10, 130))
        # showing bbox info & delete bbox
        self.lb1 = Label(self.frame, text = 'Bounding boxes:')
        self.lb1.grid(row = 3, column = 4, sticky=W+E, padx=(130, 50))


        
        self.listbox = Listbox(self.frame, width = 40, height = 12)
        self.listbox.grid(row = 4, column = 4, sticky = N+S)
        self.btnDel = Button(self.frame, text = 'Clear', command = self.delBBox)
        self.btnDel.grid(row = 5, column = 4, sticky = W+E+N)
        self.btnClear = Button(self.frame, text = 'ClearAll', command = self.clearBBox)
        self.btnClear.grid(row = 6, column = 4, sticky = W+E+N)

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 7, column = 1, columnspan = 4, sticky = W+E)
        self.conv2YoloBtn = Button(self.ctrPanel, text='Convert YOLO', width = 15, command = self.convert2Yolo)
        self.conv2YoloBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.resetChkBtn = Button(self.ctrPanel, text='ResetCheckpoint', width = 15, command = self.resetCheckpoint)
        self.resetChkBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.loadChkBtn = Button(self.ctrPanel, text='LoadCheckpoint', width = 15, command = self.loadCheckpoint) 
        self.loadChkBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.skipBtn = Button(self.ctrPanel, text ='Skip', width = 10, command = self.skipImage)
        self.skipBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)

        # example pannel for illustration
        self.egPanel = Frame(self.frame, border = 10)
        self.egPanel.grid(row = 1, column = 0, rowspan = 5, sticky = N)
        self.tmpLabel2 = Label(self.egPanel, text = "Key Shortcut :\na : Prev\nd : Next\nr : Delete BB\nv : Paste Last BB\nRight Click : Delete BB\n1-9 : Select Class")
        self.tmpLabel2.pack(side = TOP)
        self.tmpLabel3 = Label(self.egPanel, text = "\nBasic Usage :\n1.Load Image\n2.Annotate\n3.Convert Yolo")
        self.tmpLabel3.pack(side = TOP)
        self.egLabels = []
        for i in range(3):
            self.egLabels.append(Label(self.egPanel))
            self.egLabels[-1].pack(side = TOP)

        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side = RIGHT)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

    #----------------------function to display no class --------------------------------
    def display_no_class_message(self):
        if not self.cla_can_temp:
            messagebox.showwarning("Warning", "No classes available. Please create a class first.")
            return
    #------------------------------------------------------------------------------

    #Get BBox paste
    def getLastBboxSize(self):
        if self.bboxList:
            # Retrieve the last bounding box from the list
            last_bbox = self.bboxList[-1]

            # Extract coordinates
            x1, y1, x2, y2, _ = last_bbox

            # Convert coordinates to integers
            x1, y1, x2, y2 = int(float(x1)), int(float(y1)), int(float(x2)), int(float(y2))

            # Calculate and return the size
            width = x2 - x1
            height = y2 - y1
            return width, height,_
        else:
            return None

    
    def pasteLastBbox(self, event):
        if self.tkimg:
            if not self.bboxList:
                messagebox.showerror("Error", "No bounding boxes available to paste.")
                return
            try:
                # Refresh the canvas
                self.mainPanel.update_idletasks()

                size = self.getLastBboxSize()
                if size is None:
                    return

                # Calculate x, y coordinates
                x, y = self.mainPanel.canvasx(event.x), self.mainPanel.canvasy(event.y)

                # Check if bounding box is outside image boundaries
                if x < 0 or y < 0 or x + size[0] > self.tkimg.width() or y + size[1] > self.tkimg.height():
                    messagebox.showwarning("Warning", "Bounding box cannot be drawn outside the image.")
                    return

                x1, y1 = x, y
                x2, y2 = x1 + size[0], y1 + size[1]

                # Draw the bounding box
                self.bboxList.append((x1, y1, x2, y2, size[2]))
                idx_1 = self.get_class_index(size[2])
                tmpId = self.mainPanel.create_rectangle(int(x1), int(y1), int(x2), int(y2), width=2, outline=COLORS[idx_1])
                self.bboxIdList.append(tmpId)

                self.listbox.insert(END, '%s : (%d, %d) -> (%d, %d)' % (
                    size[2], x1, y1, x2, y2))
                self.listbox.itemconfig(len(self.bboxIdList) - 1, fg=COLORS[idx_1])

                # Update the total bbox label
                self.totalBboxLabel.config(text='Total BBoxes: {}'.format(len(self.bboxList)))

            except Exception as e:
                messagebox.showerror("Error", str(e))

      
	# Add this function to the LabelTool class for adding a new class
    def addNewClass(self):
        new_class = askstring("Add New Class", "Enter the name of the new class:")
        if new_class:
            if new_class in self.cla_can_temp:
                messagebox.showwarning("Warning", f"Class '{new_class}' already exists!")
            else:
                with open(self.classcandidate_filename, 'a') as class_file:
                    class_file.write(f"{new_class}\n")
                self.cla_can_temp.append(new_class)
                self.classcnt += 1
                self.classcandidate['values'] = self.cla_can_temp
                self.classcandidate.current(self.classcnt - 1)
                self.currentLabelclass = self.classcandidate.get()
                self.index = int(self.classcnt-1)
                messagebox.showinfo("Info", f"Class '{new_class}' added successfully!")        
        self.mainPanel.focus_set() # focus

    # Add the deleteClass function
    def deleteClass(self):
        if not self.cla_can_temp:
            messagebox.showwarning("Warning", "No classes available!")
            return
        selected_class = self.classcandidate.get()  
        if selected_class:
            print(selected_class,"bfore delete",self.cla_can_temp)

            confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete the class '{selected_class}'?")
            if confirmation:
                # Remove the class from the list and update the Combobox
                self.cla_can_temp.remove(selected_class)
                with open(self.classcandidate_filename, 'w') as class_file:
                    class_file.write("\n".join(self.cla_can_temp))
            
                self.classcnt -= 1
                self.classcandidate['values'] = self.cla_can_temp
                if self.classcnt > 0:
                    self.classcandidate.current(0)
                    self.currentLabelclass = self.classcandidate.get()
                else:
                    self.currentLabelclass = ''
                    self.classcandidate.set("No classes available")

            
                messagebox.showinfo("Info", f"Class '{selected_class}' deleted successfully!")
                # self.delete_lines_with_class(self.labelfilename,selected_class)
                self.delete_bbox_by_class(selected_class)

        else:
            messagebox.showwarning("Warning", "No class selected!")
        
        self.mainPanel.focus_set() # focus
    
    def delete_bbox_by_class(self, deleted_class):
        # Remove bounding boxes associated with the deleted class
        indices_to_delete = []
        for i in range(len(self.bboxList) - 1, -1, -1):
            if self.bboxList[i][-1] == deleted_class:
                # Remove the bounding box from the list and the canvas
                indices_to_delete.append(i)
                self.mainPanel.delete(self.bboxIdList[i])
                del self.bboxIdList[i]
                self.listbox.delete(i)

        # Delete corresponding lines from self.bboxList
        for index in indices_to_delete:
            del self.bboxList[index]

    def get_class_index(self, class_name):
        try:
            class_index = self.cla_can_temp.index(class_name)
            return class_index
        except ValueError:
            print(f"Class '{class_name}' not found in the list.")
            return None
################################################################################################
    #-----------------------Function For Load Directory--------------------------------
    def loadDir(self, dbg=False):
        self.imageList = []
        if not dbg:
            self.parent.focus()
            s = str(filedialog.askdirectory(initialdir=self.initial_image_dir)).split('/')[-1]
            self.category = s
        else:
            s = r'D:\workspace\python\labelGUI'
        self.imageDir = os.path.join(r'./Images', '%s' % (self.category))
        for ext in ('*.png', '*.jpg'):
            self.imageList.extend(glob.glob(os.path.join(self.imageDir, ext)))
        if len(self.imageList) == 0:
            messagebox.showinfo("Error", "No JPG/PNG images found in the specified dir!")
            print('No JPG/PNG images found in the specified dir!')
            return
        self.cur = 1
        self.total = len(self.imageList)
        self.outDir = os.path.join(r'./Result', '%s' % (self.category))
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
        self.loadImage() #Call Function to load the image
        print('%d images loaded from %s' % (self.total, self.category))
        messagebox.showinfo("Info", "%d images loaded from %s" % (self.total, self.category))
    #----------------------------------------------------------------------------------------

    #--------------------Function to load Image From Directory--------------------------------
    def loadImage(self):
        
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(imagepath)
        self.tkimg = ImageTk.PhotoImage(self.img)

        # Create a frame to hold the scrollbars and canvas
        frame = Frame(self.frame)
        frame.grid(row=1, column=1, columnspan=3, rowspan=4, sticky=W + N)

        # Create horizontal and vertical scrollbars
        hbar = Scrollbar(frame, orient=HORIZONTAL)
        vbar = Scrollbar(frame, orient=VERTICAL)

        # Create a canvas and configure it with the scrollbars
        new_mainPanel = Canvas(frame, cursor='tcross', width=1200, height=630,
                            scrollregion=(0, 0, self.tkimg.width(), self.tkimg.height()),
                            xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        # Pack the scrollbars and canvas
        hbar.pack(side=BOTTOM, fill=X)
        vbar.pack(side=RIGHT, fill=Y)
        new_mainPanel.pack(side=LEFT, expand=YES, fill=BOTH)

        # Configure the scrollbars to control the canvas
        hbar.config(command=new_mainPanel.xview)
        vbar.config(command=new_mainPanel.yview)
  

        # Bind mouse wheel event to scroll function
        new_mainPanel.bind("<MouseWheel>", self.scrollCanvas)

        # Rebind mouse click and mouse move functions
        new_mainPanel.bind("<Button-1>", self.mouseClick)
        new_mainPanel.bind("<Button-3>", self.removeBBox)
        new_mainPanel.bind("<Motion>", self.mouseMove)
        self.mainPanel.focus_set() #By calling focus_set() on a particular widget, you are designating that widget as the one that should receive keyboard events. 

        new_mainPanel.bind('v', self.pasteLastBbox) #press 'v' to get bbox of last drawn

        # Display the image on the canvas
        new_mainPanel.create_image(0, 0, image=self.tkimg, anchor=NW)


        # Update progress label and clear bounding boxes
        self.progLabel.config(text="%04d/%04d" % (self.cur, self.total))
        self.clearBBox()

        # Set the image name and label file name
        self.imagename = os.path.split(imagepath)[-1]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)   

        # Update the reference to mainPanel
        self.mainPanel = new_mainPanel
 
        # Load existing bounding boxes
        self.loadBBox()
        self.totalBboxLabel.config(text='Total BBoxes: {}'.format(len(self.bboxList)))

        print("Image loaded successfully!")

    def scrollCanvas(self, event):
        # Handle mouse wheel scrolling to scroll the canvas
        if event.delta:
            self.mainPanel.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1
            self.mainPanel.yview_scroll(move, "units")  
    #---------------------------------------------------------------------------------------------

    #----------------------------------Function to saveImage--------------------------------
    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            f.write('%d\n' %len(self.bboxList))
            for bbox in self.bboxList:
                f.write(' '.join(map(str, bbox)) + '\n')
        print('Image No. %d saved' %(self.cur))
    #------------------------------------------------------------------------------------------

    #--------------------------------------Function to return x,y cooriantes while mouse click on mainPanel canvas--------------------------------
    # def mouseClick(self, event):
    #     if self.tkimg:

    #         if event.num == 1:  # Left mouse button clicked
    #             if self.STATE['click'] == 0:
    #                 self.STATE['x'], self.STATE['y'] = event.x, event.y
    #             else:
    #                 x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
    #                 y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
    #                 self.bboxList.append((x1, y1, x2, y2, self.currentLabelclass))
    #                 self.bboxIdList.append(self.bboxId)
    #                 self.bboxId = None
    #                 self.listbox.insert(END, '%s : (%d, %d) -> (%d, %d)' % (
    #                     self.currentLabelclass, x1, y1, x2, y2))
    #                 self.listbox.itemconfig(len(self.bboxIdList) - 1, fg=COLORS[self.index])#COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
    #             self.STATE['click'] = 1 - self.STATE['click']
    #         elif event.num == 3:  # Right mouse button clicked
    #             self.removeBBox(event)

    def mouseClick(self, event):
        self.display_no_class_message()
        
        if self.tkimg:
            x = self.mainPanel.canvasx(event.x)  # Adjust for scroll position
            y = self.mainPanel.canvasy(event.y)  # Adjust for scroll position
            if event.num == 1:  # Left mouse button clicked
                if self.STATE['click'] == 0:
                    self.STATE['x'], self.STATE['y'] = x, y
                else:
                    x1, x2 = min(self.STATE['x'], x), max(self.STATE['x'], x)
                    y1, y2 = min(self.STATE['y'], y), max(self.STATE['y'], y)
                    self.bboxList.append((x1, y1, x2, y2, self.currentLabelclass))
                    self.index = self.get_class_index(self.currentLabelclass)
                    self.bboxIdList.append(self.bboxId)
                    self.bboxId = None
                    self.listbox.insert(END, '%s : (%d, %d) -> (%d, %d)' % (
                        self.currentLabelclass, x1, y1, x2, y2))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg=COLORS[self.index])

                self.STATE['click'] = 1 - self.STATE['click']
                self.totalBboxLabel.config(text='Total BBoxes: {}'.format(len(self.bboxList)))


            elif event.num == 3:  # Right mouse button clicked
                self.removeBBox(event)


    def removeBBox(self, event):
        
        x = self.mainPanel.canvasx(event.x)  # Adjust for scroll position
        y = self.mainPanel.canvasy(event.y)  # Adjust for scroll position
        selected_bbox_id = None

        for bbox_id in self.bboxIdList:
            bbox_coords = self.mainPanel.coords(bbox_id)
            lx, ly, rx, ry = bbox_coords[0], bbox_coords[1], bbox_coords[2], bbox_coords[3]

            if lx <= x <= rx and ly <= y <= ry:
                selected_bbox_id = bbox_id
                break
        if selected_bbox_id:
            bbox_index = self.bboxIdList.index(selected_bbox_id)
            self.mainPanel.delete(selected_bbox_id)
            self.bboxIdList.pop(bbox_index)
            self.bboxList.pop(bbox_index)
            self.listbox.delete(bbox_index)
            
            self.totalBboxLabel.config(text='Total BBoxes: {}'.format(len(self.bboxList)))



    #----------------------------------------------------------------------------------

    #----------------------Functon to retrun x,y coordinates whicle moving mouse over mainPanel canvas--------------------
    # def mouseMove(self, event):
    #     if self.tkimg:

    #         self.disp.config(text = 'x: %d, y: %d' %(event.x, event.y))
    #         if self.tkimg:
    #             if self.hl:
    #                 self.mainPanel.delete(self.hl)
    #             self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
    #             if self.vl:
    #                 self.mainPanel.delete(self.vl)
    #             self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
    #         if 1 == self.STATE['click']:
    #             if self.bboxId:
    #                 self.mainPanel.delete(self.bboxId)
    #             self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], \
    #                                                             event.x, event.y, \
    #                                                             width = 2, \
    #                                                             outline = COLORS[self.index])#COLORS[len(self.bboxList) % len(COLORS)])

    def mouseMove(self, event):
        self.display_no_class_message()

        if self.tkimg:
            x = self.mainPanel.canvasx(event.x)  # Adjust for scroll position
            y = self.mainPanel.canvasy(event.y)  # Adjust for scroll position


            self.disp.config(text='x: %d, y: %d' % (x, y))
            if self.tkimg:
                if self.hl:
                    self.mainPanel.delete(self.hl)
                self.hl = self.mainPanel.create_line(0, y, self.tkimg.width(), y, width=2)
                if self.vl:
                    self.mainPanel.delete(self.vl)
                self.vl = self.mainPanel.create_line(x, 0, x, self.tkimg.height(), width=2)

            if 1 == self.STATE['click']:
                if self.bboxId:
                    self.mainPanel.delete(self.bboxId)
                self.index = self.get_class_index(self.currentLabelclass)
                self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], x, y, width=2,
                                                            outline=COLORS[self.index])
        

    

    #--------------------------------------------------------------------------------------------------------------------------    

    #--------------------------Delete Selected BBox ------------------------
    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)
        self.mainPanel.focus_set() # focus
    #----------------------------------------------------------------

    #-----------------------Clear All Bboxes ------------------------
    def clearBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []
        self.mainPanel.focus_set() #focus


    def clearBBoxShortcut(self, event):
        if self.bboxList:
            answer = messagebox.askquestion("Clear Bbox", "Are you sure you want to clear all Bbox?")
            
            if answer == "yes":
                for idx in range(len(self.bboxIdList)):
                    self.mainPanel.delete(self.bboxIdList[idx])

                self.listbox.delete(0, len(self.bboxList))
                self.bboxIdList = []
                self.bboxList = []
        else:
            messagebox.showinfo("Nothing to Delete", "No Bbox to delete.")
    #----------------------------------------------------------------

    #--------------------If we have drawn bbox previously then it will retrieve that bbox----------------------------------------------------------------
    
        # Add this function to the LabelTool class for adding a new class if it doesn't already exist
    def addNewClass_(self, new_class):
            create_new_class = messagebox.askyesno("Found New Class", f"Do you want to add a new class '{new_class}'?")
            if create_new_class:
                with open(self.classcandidate_filename, 'a') as class_file:
                    class_file.write(f"{new_class}\n")

                self.cla_can_temp.append(new_class)
                self.classcnt += 1
                self.classcandidate['values'] = self.cla_can_temp
                self.classcandidate.current(self.classcnt - 1)
                self.currentLabelclass = self.classcandidate.get()
                self.index = int(self.classcnt-1)
                messagebox.showinfo("Info", f"Class '{new_class}' added successfully!")
            else:
                # User chose not to create the new class, so delete lines with this class from the file
                self.delete_lines_with_class(self.labelfilename, new_class)

    def delete_lines_with_class(self, filename, class_name):
        with open(filename, 'r') as file:
            lines = file.readlines()

        with open(filename, 'w') as file:
            for line in lines:
                if class_name not in line:
                    file.write(line)
    
    def check_and_create_new_classes(self, class_list_from_file):
        new_classes = set(class_list_from_file) - set(self.cla_can_temp)
        if new_classes:
            print(f"New classes found: {', '.join(new_classes)}")

            for new_class in new_classes:
                self.addNewClass_(new_class)
            else:
                print("No new classes created.")
        else:
            print("No new classes found.")
            return None




    def return_all_class_list_from_file(self):
        class_list_from_file = []
        if os.path.exists(self.labelfilename):
            unique_classes = set()
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    if i == 0:
                        continue
                    class_name = line.split()[-1]
                    unique_classes.add(class_name)

            class_list_from_file = list(unique_classes)

        self.check_and_create_new_classes(class_list_from_file) #Function called to check if class exists or not

                            
                            

    def loadBBox(self):
        self.return_all_class_list_from_file()
        # print("Loading bbox",COLORS[self.index])
		
		
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    if i == 0:
                        self.bbox_cnt = int(line.strip())
                        continue
                    # tmp = [int(t.strip()) for t in line.split()]
                    tmp = line.split()
                    self.bboxList.append(tuple(tmp))
                    idx = self.bboxList[i-1][-1]
                    idx_1 = self.get_class_index(idx)
                    self.index = idx_1
                    tmpId = self.mainPanel.create_rectangle(int(float(tmp[0])), int(float(tmp[1])), \
                                        int(float(tmp[2])), int(float(tmp[3])), \
                                        width=2, outline=COLORS[idx_1])
										 #COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    self.bboxIdList.append(tmpId)
                    self.listbox.insert(END, '%s : (%d, %d) -> (%d, %d)' %(tmp[4],int(float(tmp[0])), int(float(tmp[1])), \
                    												  int(float(tmp[2])), int(float(tmp[3]))))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[idx_1] )#COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])

    
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #-------------------------------function is used to resume the annotation process from the image index specified in the "log/checkpoint.txt" file-----------------------
    def loadCheckpoint(self, event = None):
        checkpoint = 0
        with open("log/checkpoint.txt","r") as checkpointFile:
            checkpoint = checkpointFile.read()
        if 1 <= int(checkpoint) and int(checkpoint) <= self.total:
            self.cur = int(checkpoint)
            self.loadImage()
    #----------------------------------------------------------------To Reset Checkpoint----------------------------------------------------------------
    def resetCheckpoint(self, event=None):
        if self.cur == 0 or self.cur==1:
            print("Already at the first image. No need to reset.")
            # You can display a messagebox or any other appropriate warning mechanism.
        else:
            with open("log/checkpoint.txt", "w") as checkpointFile:
                checkpointFile.write("1")
            # Load the image associated with the reset checkpoint
            self.cur = 1
            self.loadImage()

    #--------------------------------------------------------------------------------------------------------------------------------

    #-----------------------------Previous Image Load, next Image Load, skip Image, or which index image you want to load----------------------------------------------------------------,
    def prevImage(self, event=None):
        # self.bboc_cnt = 0
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()
        else:
            messagebox.showinfo("Info", "Already at the first image")

    def nextImage(self, event=None):
        # self.bboc_cnt = 0
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        else:
            messagebox.showinfo("Info", "Already at the last image")
            # Optionally, you can reset the checkpoint to the first image
            # self.resetCheckpoint()
            
    def skipImage(self, event = None):
        # self.bboc_cnt = 0
        #os.remove(self.imageList[self.cur - 1])
        print(self.imageList[self.cur - 1]+" is skipped.")
        with open("log/skipped.txt",'a') as skippedFile:
            skippedFile.write("{}\n".format(self.imageList[self.cur - 1]))
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def gotoImage(self):
        # self.bboc_cnt = 0
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()
    #--------------------------------------------------------------------------------------------------------------------------------

    #--------------Function to choose which class you want to switch----------------------------------------------------------------
    def setClass(self, event):
            self.currentLabelclass = self.classcandidate.get()
            print('set label class to :',self.currentLabelclass)
            self.index = self.get_class_index(self.currentLabelclass)
            print(self.index)
            self.mainPanel.focus_set() # focus
            
    def setClassShortcut(self, event):
        if event.char.isdigit():
            idx = int(event.char) - 1
            if 0 <= idx < len(self.cla_can_temp):
                self.classcandidate.current(idx)
                self.currentLabelclass = self.classcandidate.get()
                self.index = self.get_class_index(self.currentLabelclass)
                print(self.index)
                print('set label class to:', self.currentLabelclass)
            else:
                messagebox.showerror("Error", "Invalid class index")

    #--------------------------------------------------------------------------------------------------------------------------------

    #-------------------------------------------------Convert the bbox to yolo format----------------------------------------------------------------
    def convert2Yolo(self, event = None):
        if (self.category == ''):
            messagebox.showinfo("Error", "Please Annotate Image first")
        else:
            outpath = "./Result_YOLO/" + self.category +'/'
            convert.Convert2Yolo(self.outDir+'/', outpath, self.category, self.cla_can_temp)
            messagebox.showinfo("Info", "YOLO data format conversion done")
    #--------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
    root.resizable(width =  True, height = True)
    root.mainloop()