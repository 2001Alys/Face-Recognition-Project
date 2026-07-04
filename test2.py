#bawienie się target_size, margin, minNeighbors w celu uzyskania jak najlepszych wyników,

import time
import cv2

def resize_image(image_path, target_size, maintain_aspect_ratio=True):
    start_resize = time.time()
    img = cv2.imread(image_path)
    
    if maintain_aspect_ratio:
        original_height, original_width = img.shape[:2]
        aspect_ratio = original_width / original_height

        if original_width > original_height:
            new_width = target_size
            new_height = int(target_size / aspect_ratio)
        else:
            new_height = target_size
            new_width = int(target_size * aspect_ratio)
    else:
        new_width = target_size
        new_height = target_size

    resized_img = cv2.resize(img, (new_width, new_height))
    resize_time = time.time() - start_resize
    return resized_img, resize_time

def detect_faces_opencv(gray_image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    start_time = time.time()
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=6)
    opencv_time = time.time() - start_time
    
    return faces, opencv_time

def main(image_path):
    print("\n====================================")
    print(f"Przetwarzanie obrazu: {image_path}")

    resized_image, resize_time = resize_image(image_path, target_size=1000)
    gray_image_resized = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    opencv_faces_resized, opencv_time_resized = detect_faces_opencv(gray_image_resized)

    total_time_resized = resize_time + opencv_time_resized
    print("\nTest 1: Z resizowaniem i bez wyszarzenia")
    print(f"OpenCV wykrył {len(opencv_faces_resized)} twarzy w {opencv_time_resized:.4f} sekund.")
    print(f"Suma: {total_time_resized:.4f} sekund.")

    start_gray = time.time()
    gray_image_resized = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    gray_time = time.time() - start_gray

    opencv_faces_resized_gray, opencv_time_resized_gray = detect_faces_opencv(gray_image_resized)

    total_time_resized_gray = resize_time + gray_time + opencv_time_resized_gray
    print("\nTest 2: Z resizowaniem i z wyszarzeniem")
    print(f"OpenCV wykrył {len(opencv_faces_resized_gray)} twarzy w {opencv_time_resized_gray:.4f} sekund.")
    print(f"Suma: {total_time_resized_gray:.4f} sekund.")

main('alys1.jpg')