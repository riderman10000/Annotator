# Annotator - Image Annotation Tool

License: MIT License

## Description
To label the object, annotator is a program that provides a fundamental code basis to extract the coordinates/location of object in an image.

## Key Features
While the main feature is the code basis for easy implementation of methods to export lables in various data format to create dataset. Some of the updates from its previous versions are: 
- seperated gui and tool code
- menu bar to include desired methods 
- add your export ways and techniques to the object
- shortcuts: keyboard and mouse, including mouse pressed and released

## Main Program and Credits
- Main Program forked from [puzzledqs/BBox-Label-Tool](https://github.com/puzzledqs/BBox-Label-Tool/tree/multi-class)
- Converter to YOLO format forked from [ManivannanMurugavel/YOLO-Annotation-Tool](https://github.com/ManivannanMurugavel/YOLO-Annotation-Tool)
- inspired from rukesh duwal [Yolo-Annotator](https://github.com/iamrukeshduwal/Yolo_Annotator.git) 

## Usage
1. clone this repo
2. run the python file rl_main.py # this is for development only will change to main once some parts are final
3. now use the open image directory to navigate to the image file (mostly extracts .jpg and .png extension image, you can add more in the code)
4. The image will appear in the center of the program. Create a class for the object to label  
5. currently supports rectangle bounding box, so point to the left-top of the object, and drag your mouse to the bottom-right of the object. 

## License
This project is open-source and currently does not have a specific license. You are free to view, use, and modify the code for personal or educational purposes. If you plan to distribute or use this project in a commercial product, please consider adding an appropriate open-source license.


