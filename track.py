import cv2
import numpy as np

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
output_layer_names = net.getUnconnectedOutLayersNames()

# Load classes
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Open a connection to the webcam (0 represents the default camera)
cap = cv2.VideoCapture(0)

# Container dimensions
container_rows = 8
container_cols = 8
container_size = container_rows * container_cols

# Initialize counts
total_tires = 0
occupied_space = 0

while True:
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layer_names)

    # Extracting information from detection
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 67:  # Assuming class 67 corresponds to 'tyre' in COCO
                # Object detected
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype(int)
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Process detected objects
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            occupied_space += w * h
            total_tires += 1
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Calculate remaining space
    remaining_space = max(container_size - occupied_space, 0)

    # Display counts and remaining space
    print(f"Total Tires: {total_tires}, Occupied Space: {occupied_space}, Remaining Space: {remaining_space}")

    # Display the frame
    cv2.imshow("Frame", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
