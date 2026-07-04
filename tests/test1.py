#porównanie obróbki obrazu dla modelu wykrywania twarzy,
#wygrywa OpenCV

import time
import cv2
import face_recognition
from deepface import DeepFace

def resize_image(image_path, target_size, maintain_aspect_ratio=True):
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

    return cv2.resize(img, (new_width, new_height))

def detect_faces_opencv(gray_image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    start_time = time.time()
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    opencv_time = time.time() - start_time
    
    return faces, opencv_time

def detect_faces_face_recognition(gray_image):
    start_time = time.time()
    face_locations = face_recognition.face_locations(gray_image)
    face_recognition_time = time.time() - start_time
    
    return face_locations, face_recognition_time

def detect_faces_deepface(image_path):
    start_time = time.time()
    faces = DeepFace.extract_faces(img_path=image_path, enforce_detection=False)
    deepface_time = time.time() - start_time
    
    return faces, deepface_time

def detect_faces(image_path, target_size=1000):
    resized_image = resize_image(image_path, target_size)
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    temp_gray_image_path = 'temp_gray_image.jpg'
    cv2.imwrite(temp_gray_image_path, gray_image)

    opencv_faces, opencv_time = detect_faces_opencv(gray_image)
    face_recognition_faces, face_recognition_time = detect_faces_face_recognition(gray_image)
    deepface_faces, deepface_time = detect_faces_deepface(image_path)
    
    import os
    os.remove(temp_gray_image_path)

    return (opencv_faces, opencv_time), (face_recognition_faces, face_recognition_time), (deepface_faces, deepface_time)

def main(image_path):
    print(f"Przetwarzanie obrazu: {image_path}\n")

    print("Test 1: Bez resizowania i bez wyszarzenia")
    original_image = cv2.imread(image_path)
    
    opencv_faces, opencv_time = detect_faces_opencv(original_image)
    face_recognition_faces, face_recognition_time = detect_faces_face_recognition(original_image)
    deepface_faces, deepface_time = detect_faces_deepface(image_path)

    print(f"OpenCV wykrył {len(opencv_faces)} twarzy w {opencv_time:.4f} sekund.")
    print(f"face_recognition wykrył {len(face_recognition_faces)} twarzy w {face_recognition_time:.4f} sekund.")
    print(f"DeepFace wykrył {len(deepface_faces)} twarzy w {deepface_time:.4f} sekund.")

    print("\nTest 2: Z resizowaniem i bez wyszarzenia")
    resized_image = resize_image(image_path, target_size=1000)
    gray_image_resized = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    
    opencv_faces_resized, opencv_time_resized = detect_faces_opencv(gray_image_resized)
    face_recognition_faces_resized, face_recognition_time_resized = detect_faces_face_recognition(gray_image_resized)
    deepface_faces_resized, deepface_time_resized = detect_faces_deepface(image_path)

    print(f"OpenCV wykrył {len(opencv_faces_resized)} twarzy w {opencv_time_resized:.4f} sekund.")
    print(f"face_recognition wykrył {len(face_recognition_faces_resized)} twarzy w {face_recognition_time_resized:.4f} sekund.")
    print(f"DeepFace wykrył {len(deepface_faces_resized)} twarzy w {deepface_time_resized:.4f} sekund.")

    print("\nTest 3: Bez resizowania i z wyszarzeniem")
    gray_image_original = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    
    opencv_faces_gray, opencv_time_gray = detect_faces_opencv(gray_image_original)
    face_recognition_faces_gray, face_recognition_time_gray = detect_faces_face_recognition(gray_image_original)
    deepface_faces_gray, deepface_time_gray = detect_faces_deepface(image_path)

    print(f"OpenCV wykrył {len(opencv_faces_gray)} twarzy w {opencv_time_gray:.4f} sekund.")
    print(f"face_recognition wykrył {len(face_recognition_faces_gray)} twarzy w {face_recognition_time_gray:.4f} sekund.")
    print(f"DeepFace wykrył {len(deepface_faces_gray)} twarzy w {deepface_time_gray:.4f} sekund.")

    print("\nTest 4: Z resizowaniem i z wyszarzeniem")
    gray_image_resized = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    
    opencv_faces_resized_gray, opencv_time_resized_gray = detect_faces_opencv(gray_image_resized)
    face_recognition_faces_resized_gray, face_recognition_time_resized_gray = detect_faces_face_recognition(gray_image_resized)
    deepface_faces_resized_gray, deepface_time_resized_gray = detect_faces_deepface(image_path)

    print(f"OpenCV wykrył {len(opencv_faces_resized_gray)} twarzy w {opencv_time_resized_gray:.4f} sekund.")
    print(f"face_recognition wykrył {len(face_recognition_faces_resized_gray)} twarzy w {face_recognition_time_resized_gray:.4f} sekund.")
    print(f"DeepFace wykrył {len(deepface_faces_resized_gray)} twarzy w {deepface_time_resized_gray:.4f} sekund.")

main('alys1.jpg')