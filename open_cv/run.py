import cv2
import numpy as np

# Tải bộ phân loại Haar Cascade cho nhận diện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

def get_dominant_color_name(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    hist = cv2.calcHist([h], [0], None, [180], [0, 180])
    dominant_hue = np.argmax(hist)

    # Xác định tên màu dựa trên giá trị hue
    if 0 <= dominant_hue < 10 or 160 <= dominant_hue <= 180:
        return "Đỏ"
    elif 10 <= dominant_hue < 25:
        return "Cam"
    elif 25 <= dominant_hue < 35:
        return "Vàng"
    elif 35 <= dominant_hue < 85:
        return "Xanh lá"
    elif 85 <= dominant_hue < 130:
        return "Xanh dương"
    elif 130 <= dominant_hue < 160:
        return "Tím"
    else:
        return "Không xác định"

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Chuyển sang ảnh xám
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Vẽ hình chữ nhật quanh khuôn mặt
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Xác định vùng áo dưới khuôn mặt
        shirt_x1 = x - int(0.15 * w)
        shirt_x2 = x + w + int(0.15 * w)
        shirt_y1 = y + h
        shirt_y2 = y + h + int(1.2 * h)

        # Đảm bảo không vượt quá khung hình
        shirt_x1 = max(shirt_x1, 0)
        shirt_x2 = min(shirt_x2, frame.shape[1])
        shirt_y2 = min(shirt_y2, frame.shape[0])

        # Vẽ hình chữ nhật vùng áo
        cv2.rectangle(frame, (shirt_x1, shirt_y1), (shirt_x2, shirt_y2), (255, 0, 0), 2)
        
        # Crop vùng áo
        shirt_crop = frame[shirt_y1:shirt_y2, shirt_x1:shirt_x2]
        if shirt_crop.size > 0:
            print("Size áo của cổ: ", shirt_crop.size)
            cv2.imshow('Shirt Crop', shirt_crop)
            color_name = get_dominant_color_name(shirt_crop)
            print(color_name)
            print(f"Màu chủ đạo của áo: {color_name}")
            break
        break

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == 27:  # Nhấn 'Esc' để thoát
        break

cap.release()
cv2.destroyAllWindows()