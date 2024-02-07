# YOLO Annotator - Image Annotation Tool

Author: Rukesh Duwal
Date: January 30th, 2024
Occupation: Computer Vision Engineer at Crimson Tech
License: MIT License

## Description

The YOLO Annotator is a simple image annotation tool developed in Python using Tkinter for graphical user interface elements.

## Key Features

- Annotation of bounding boxes.
- Keyboard shortcuts for quick navigation.

## Main Program and Credits

- Main Program forked from [puzzledqs/BBox-Label-Tool](https://github.com/puzzledqs/BBox-Label-Tool/tree/multi-class)
- Converter to YOLO format forked from [ManivannanMurugavel/YOLO-Annotation-Tool](https://github.com/ManivannanMurugavel/YOLO-Annotation-Tool)

## Usage

1. Run `python main.py`.
2. Click `LoadImage`, select a folder that contains a list of images.
3. For multi-class tasks, modify 'class.txt' with your class candidates. Before labeling a bounding box, choose the 'Current Class' in the Combobox or by pressing <kbd>1-9</kbd> on your keyboard.
4. To create a new bounding box, left-click to select the first vertex. Move the mouse to draw a rectangle and left-click again to select the second vertex.
   - To delete the existing bounding box while drawing, press <kbd>right click inside respective bbox</kbd> or select it from the listbox and click `Clear`<kbd>
   - To delete all existing bounding boxes in the image, click `ClearAll` or press <kbd>r</kbd>.
5. After finishing one image, click `Next` or press <kbd>d</kbd> to advance. Click `Prev` or press <kbd>a</kbd> to reverse. Alternatively, input the index and click `Go` to navigate to an arbitrary image.
   - The labeling result will be saved in **Labels/[folder name]/..** only if the 'Next' button is clicked.
   - **The checkpoint of the last Image Number will be saved when the 'Next' button is clicked.**
6. Click `Skip` to skip an unwanted image from the directory and skip the annotation for that image (the skipped image path will be saved in log/skip.txt).
7. Click `ConvertYOLO` or press <kbd>c</kbd> to convert the labeling result to YOLO format. The result will be saved in **Result_YOLO/[folder name]/..**.
8. Use the 'Add Class' and 'Delete Class' buttons in the UI to manage classes dynamically.

## Additional Features

- **Bounding Box Count**: The tool provides the count of the number of bounding boxes drawn inside image.
- **Color Assignment**: Each class is assigned a unique color for better visualization.
- **Paste Last Bounding Box**: Press 'v' to paste the last drawn bounding box where the mouse pointer is located.
- **Paste Last Bounding Box From Previous Image**: Press 'b' to paste the last drawn bounding box from previous image where the mouse pointer is located.
- **Scroll Support**: Users can scroll horizontally and vertically for larger images.

## How to Run

1. Make sure you have Python installed on your system.
2. Clone this repository:
   git clone https://github.com/iamrukeshduwal/Yolo_Annotator.git
3. cd Yolo_Annotator
4. python main.py

## License
This project is open-source and currently does not have a specific license. You are free to view, use, and modify the code for personal or educational purposes. If you plan to distribute or use this project in a commercial product, please consider adding an appropriate open-source license.


