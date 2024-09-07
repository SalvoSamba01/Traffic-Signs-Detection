import cv2
import os

class_names = [
    'animals',
    'bend',
    'bend-left', 
    'bend-right', 
    'construction', 
    'cycles-crossing', 
    'danger', 
    'give-way', 
    'go-left', 
    'go-left-or-straight', 
    'go-right', 
    'go-right-or-straight', 
    'go-straight', 
    'keep-left', 
    'keep-right', 
    'no-entry', 
    'no-overtaking', 
    'no-overtaking-trucks-', 
    'no-traffic-both-ways', 
    'no-trucks', 
    'pedestrian-crossing', 
    'priority-at-next-intersection', 
    'priority-road', 
    'restriction-ends', 
    'restriction-ends-80', 
    'road-narrows', 
    'roundabout', 
    'school-crossing', 
    'slippery-road', 
    'speed-limit-100', 
    'speed-limit-20', 
    'speed-limit-30', 
    'speed-limit-50', 
    'speed-limit-60', 
    'speed-limit-70', 
    'speed-limit-80', 
    'stop', 
    'traffic-signal', 
    'uneven-road'
]

images_folder = "./yolov10/datasets/TrafficSigns/images/test" # image folder
labels_folder = "./yolov10/datasets/TrafficSigns/labels/test" # label folder

output_folder = os.path.join("./yolov10/datasets/TrafficSigns/groundThruthAnnotations", 'test')
os.makedirs(output_folder, exist_ok=True)
i=0
for image_file in os.listdir(images_folder):
    i+=1     
    print(f'Processing image {i} of {len(os.listdir(images_folder))}')
    if image_file.endswith('.jpg') or image_file.endswith('.png'):
        image_path = os.path.join(images_folder, image_file)
        label_path = os.path.join(labels_folder, image_file.replace('.jpg', '.txt').replace('.png', '.txt'))

        image = cv2.imread(image_path)
        h, w = image.shape[:2]  

        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                # YOLO format: class_id, x_center, y_center, width, height (normalized)
                data = line.strip().split()
                class_id = int(data[0])
                x_center, y_center, bbox_width, bbox_height = map(float, data[1:])

                x_center = int(x_center * w)
                y_center = int(y_center * h)
                bbox_width = int(bbox_width * w)
                bbox_height = int(bbox_height * h)

                x1 = int(x_center - bbox_width / 2)
                y1 = int(y_center - bbox_height / 2)
                x2 = int(x_center + bbox_width / 2)
                y2 = int(y_center + bbox_height / 2)

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                label = class_names[class_id]
                font = cv2.FONT_HERSHEY_DUPLEX
                font_scale = 0.7
                font_thickness = 1
                (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)

                text_x = int(x1 + (x2 - x1 - text_width) / 2)
                text_y = int(y1)-10  

                cv2.putText(image, label, (text_x, text_y), font, font_scale, (255, 0, 0), font_thickness)
                
        output_image_path = os.path.join(output_folder, image_file)
        cv2.imwrite(output_image_path, image)

cv2.destroyAllWindows()