import time
import cv2
import face_recognition
import PySimpleGUI as sg

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

#porownanie face_recog
def encode_face(face):
    try:
        face_encoding = face_recognition.load_image_file(face)
        encoding = face_recognition.face_encodings(face_encoding)[0]
        
        return encoding
    except Exception as e:
        print(f"Błąd w porównaniu face_recognition: {e}")
        return False

#porownanie face_recog
def compare_faces_face_recognition(encoding_1, encoding_2):
    try:
        results = face_recognition.compare_faces([encoding_1], encoding_2, tolerance=0.6)
        
        return results[0]
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
            trimmed_faces = []
            
            for i, (x, y, w, h) in enumerate(selected_faces):
                face = resized_image[y:y+h, x:x+w]
                scaled_face = cv2.resize(face, (220, 220), interpolation=cv2.INTER_LINEAR)
                trimmed_faces.append(scaled_face)
                cv2.imwrite('picture.jpg', scaled_face)
            
        else:
            sg.popup("Brak twarzy w pobliżu środka z marginesem. Spróbuj ponownie.")
            return None
    else:
        sg.popup("Na zdjęciu nie wykryto twarzy. Spróbuj zrobić zdjęcie ponownie.")
        return None
    
    total_time = time.time() - start_total_time
    print(f"Wykryto twarze w czasie: {opencv_time_resized:.4f} sekund.\n")
    print(f"Suma czasu na operacje wykrycia twarzy: {total_time:.4f} sekund.\n")
    
    return trimmed_faces