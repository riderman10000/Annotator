import os  
import glob 
import json 

shape_info = {
    'label':None,
    'points':[],
    'shape_type': None,
    'group_ids': None, 
}
file_json_info = {
    'version': "",
    'shapes': [], # self.shape_info
    'image_name': None, 
    'imageHeight': None,
    'imageWidth': None,
}
DEBUG = True 

def convert_yolo_to_voc(image, yolo_format, for_albumentation = False):
    image_height, image_width, channels = image.shape 
    obj_class, norm_x, norm_y, norm_w, norm_h = yolo_format 

    width = int(norm_w * image_width)
    height = int(norm_h * image_height)

    x1 = int(((2 * norm_x * image_width) - width)/2) 
    x2 = x1 + width 

    y1 = int(((2 * norm_y * image_height) - height)/2) 
    y2 = y1 + height
    if for_albumentation:
        return x1, y1, x2, y2, obj_class
    return obj_class, x1, y1, x2, y2

def convert_voc_to_yolo(image_height_width_info, voc_format):
    image_height, image_width = image_height_width_info 
    obj_class, x1, y1, x2, y2 = voc_format

    norm_w = (x2 - x1)/image_width
    norm_h = (y2 - y1)/image_height

    norm_x = (x2 + x1)/(2 * image_width)
    norm_y = (y2 + y1)/(2 * image_height)
    return obj_class, norm_x, norm_y, norm_w, norm_h

def export_yolo_from_directory(json_directory, save_file_directory = None):
    image_json_path_list = glob.glob(os.path.join(json_directory, "*.json"))
    for image_json_path in image_json_path_list:
        converted_bbox_infos = []
        with open(image_json_path, 'r') as image_json_file:
            image_file_json_info = json.load(image_json_file)

            if image_file_json_info['version'] == "1.0.0":
                image_height, image_width = image_file_json_info['imageHeight'], image_file_json_info['imageWidth']
                for shape in image_file_json_info['shapes']:
                    if shape['shape_type'] == 'rectangle':
                        obj_class, norm_x, norm_y, norm_w, norm_h = convert_voc_to_yolo(
                            (image_height, image_width),
                            [shape['label']] + shape['points'] )
                        converted_bbox_infos.append([obj_class, norm_x, norm_y, norm_w, norm_h])

        if len(converted_bbox_infos):
            image_label = image_json_path.replace('.json', '.txt')
            with open(image_label, 'w+') as label_file_obj:
                for bbox_info in converted_bbox_infos:
                    obj_class, norm_x, norm_y, norm_w, norm_h = bbox_info
                    if DEBUG:
                        print('[+] export yolo {obj_class} {norm_x} {norm_y} {norm_w} {norm_h}\n'.format(
                            obj_class=obj_class, norm_x=norm_x, norm_y= norm_y, norm_w = norm_w, norm_h = norm_h))
                    label_file_obj.write('\"{obj_class}\" {norm_x} {norm_y} {norm_w} {norm_h}\n'.format(
                            obj_class=obj_class, norm_x=norm_x, norm_y= norm_y, norm_w = norm_w, norm_h = norm_h))
                ...
    ...