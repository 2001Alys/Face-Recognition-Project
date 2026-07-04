#porównanie modeli porównania twarzy dla przygotowanych i nieprzygotowanych obrazów,
#wygrywa face_recognition,

import time
import cv2
from deepface import DeepFace
import face_recognition
import matplotlib.pyplot as plt

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#zmiana rozdzielczosci obrazu
def resize_image(image_path, target_size, maintain_aspect_ratio=True):
    start_resize = time.time()
    
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Nie udało się wczytać obrazu. Sprawdź ścieżkę do pliku.")
    
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

    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    resize_time = time.time() - start_resize
    return resized_img, resize_time

#wykrycie kilku twarzy,
def detect_faces_opencv(gray_image):
    start_time = time.time()
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=6)
    opencv_time = time.time() - start_time
    return faces, opencv_time

#filtorowanie i sortowanie twarzy,
def choose_faces_within_margin(faces, image_width, image_height, margin=400):
    center_x, center_y = image_width / 2, image_height / 2
    face_distances = []
    
    for (x, y, w, h) in faces:
        face_center_x = x + w / 2
        face_center_y = y + h / 2
        
        distance_squared = (face_center_x - center_x) ** 2 + (face_center_y - center_y) ** 2
        
        if distance_squared <= margin ** 2:
            face_distances.append(((x, y, w, h), distance_squared))
    
    face_distances.sort(key=lambda face: face[1])
    return [face[0] for face in face_distances]

#przycięcie twarzy z obrazów
def plot_faces(image, faces, filename):
    plt.figure(figsize=(10, 10))
    trimmed_faces = []
    for (i, (x, y, w, h)) in enumerate(faces):
        face = image[y:y+h, x:x+w]
        trimmed_faces.append(face)
        plt.subplot(1, len(faces), i + 1)
        plt.imshow(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
        plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    
    return trimmed_faces

#porownanie deepface
def compare_faces_deepface(face1_path, face2_path):
    try:
        start_time = time.time()
        result = DeepFace.verify(face1_path, face2_path, model_name="Facenet", enforce_detection=True)
        comparison_time = time.time() - start_time
        return result['verified'], comparison_time
    except Exception as e:
        print(f"Błąd w porównaniu DeepFace: {e}")
        return False, 0

#porownanie face_recog
def compare_faces_face_recognition(face1_encoding, face2_encoding):
    try:
        start_time = time.time()
        face1_encoding = face_recognition.load_image_file(face1_encoding)
        face2_encoding = face_recognition.load_image_file(face2_encoding)
        encoding_1 = face_recognition.face_encodings(face1_encoding)[0]
        encoding_2 = face_recognition.face_encodings(face2_encoding)[0]
        results = face_recognition.compare_faces([encoding_1], encoding_2)
        comparison_time = time.time() - start_time
        return results[0], comparison_time
    except Exception as e:
        print(f"Błąd w porównaniu face_recognition: {e}")
        return False, 0
    
#przygotowanie twarzy do porównania
def prepare_image(image_path):
    print("====================================")
    print(f"Przetwarzanie obrazu: {image_path}")

    start_total_time = time.time()
    
    resized_image, resize_time = resize_image(image_path, target_size=1000)
    
    gray_image_resized = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    
    faces_resized, opencv_time_resized = detect_faces_opencv(gray_image_resized)
    
    if len(faces_resized) > 0:
        image_height, image_width = gray_image_resized.shape[:2]
        selected_faces = choose_faces_within_margin(faces_resized, image_width, image_height, margin=400)
        
        if len(selected_faces) > 0:
            print(f"Znaleziono {len(selected_faces)} twarze w odległości marginesu od środka.")
            trimmed_faces = plot_faces(resized_image, selected_faces, f'picture{image_path}')
        else:
            print("Brak twarzy w pobliżu środka z marginesem.")
            return
    else:
        print("Nie wykryto twarzy na obrazie.")
        return
    
    total_time = time.time() - start_total_time
    print(f"Wykryto twarze w czasie: {opencv_time_resized:.4f} sekund.\n")
    print(f"Suma czasu na operacje wykrycia twarzy: {total_time:.4f} sekund.\n")
    
    return trimmed_faces

def compare_faces(image1_path, image2_path):
    image1_faces = prepare_image(image1_path)
    image2_faces = prepare_image(image2_path)
    
    print("Porównanie twarzy z wczeniejszym przygotowaniem obrazów.")
    
    verified, time_taken = compare_faces_deepface(image1_faces[0], image2_faces[0])
    print("\nDeepface:")
    print(f"Ta sama osoba? {verified}")
    print(f"Porównano twarze w czasie: {time_taken:.2f} sekund")
    
    verified, time_taken = compare_faces_face_recognition(f'picture{image1_path}', f'picture{image2_path}')
    print("\nFace Recog:")
    print(f"Ta sama osoba? {verified}")
    print(f"Porównano twarze w czasie: {time_taken:.2f} sekund")
    
    print("\nPorównanie twarzy bez przygotowania obrazów.")
    
    verified, time_taken = compare_faces_deepface(image1_path, image2_path)
    print("\nDeepface:")
    print(f"Ta sama osoba? {verified}")
    print(f"Porównano twarze w czasie: {time_taken:.2f} seconds")
    
    verified, time_taken = compare_faces_face_recognition(image1_path, image2_path)
    print("\nFace Recog:")
    print(f"Ta sama osoba? {verified}")
    print(f"Porównano twarze w czasie: {time_taken:.2f} sekund")
    
compare_faces('alys1.jpg', 'alys2.jpg')

#można zmodyfikować: target_size, margin, minNeighbors,
#usunąć zapisy do plików, poprawić porównywanie face_recognition,
#lista wycinków zdjęcia może mieć kilka twarzy,