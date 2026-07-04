#porównanie funkcji modelu face_recognition dla datasetu już przyciętych twarzy, więc nie trzeba robić przygotowania obrazów,
#wygrywa face_recognition,

import time
import face_recognition
from sklearn.datasets import fetch_lfw_pairs
import numpy as np

# Funkcja konwertująca obrazy do RGB
def preprocess_image(image):
    if len(image.shape) == 2:
        image = np.stack((image,) * 3, axis=-1)
    image = (image * 255).astype(np.uint8)
    return image

# Porównanie twarzy przy użyciu face_recognition
def compare_faces_face_recognition_compare_faces(face1, face2):
    try:
        start_time = time.time()
        
        # Wykrywanie twarzy na obu obrazach
        face_locations_1 = face_recognition.face_locations(np.array(face1))
        face_locations_2 = face_recognition.face_locations(np.array(face2))
        
        # Zliczanie wykrytych twarzy
        detected_faces = len(face_locations_1) + len(face_locations_2)
        
        encoding_1 = face_recognition.face_encodings(np.array(face1), known_face_locations=face_locations_1)[0]
        encoding_2 = face_recognition.face_encodings(np.array(face2), known_face_locations=face_locations_2)[0]
        results = face_recognition.compare_faces([encoding_1], encoding_2)
        comparison_time = time.time() - start_time
        return results[0], comparison_time, detected_faces
    except Exception:
        return False, 0, 0
    
#porownanie face_recog
def compare_faces_face_recognition_face_distance(face1, face2):
    try:
        start_time = time.time()
        
        # Wykrywanie twarzy na obu obrazach
        face_locations_1 = face_recognition.face_locations(np.array(face1))
        face_locations_2 = face_recognition.face_locations(np.array(face2))
        
        # Zliczanie wykrytych twarzy
        detected_faces = len(face_locations_1) + len(face_locations_2)
        
        encoding_1 = face_recognition.face_encodings(np.array(face1), known_face_locations=face_locations_1)[0]
        encoding_2 = face_recognition.face_encodings(np.array(face2), known_face_locations=face_locations_2)[0]
        distances = face_recognition.face_distance([encoding_1], encoding_2)
        results = distances[0] < 0.5
        comparison_time = time.time() - start_time
        return results, comparison_time, detected_faces
    except Exception:
        return False, 0, 0

# Funkcja porównująca twarze w obu modelach i zbierająca statystyki
def compare_faces(image1, image2, grade, model_name):
    face1 = preprocess_image(image1)
    face2 = preprocess_image(image2)

    # Porównanie w face_recognition
    if model_name == "Face Recognition1":
        verified, time_taken, detected_faces = compare_faces_face_recognition_compare_faces(face1, face2)
    elif  model_name == "Face Recognition2":
        verified, time_taken, detected_faces = compare_faces_face_recognition_face_distance(face1, face2)
        
    correct = (verified == grade)
    return correct, time_taken, detected_faces

# Zbieranie statystyk dla modelu
def evaluate_model(model_name, lfw_pairs, num_pairs):
    correct_count = 0
    wrong_count = 0
    total_time = 0
    times = []
    total_faces_detected = 0
    
    for pair_index in range(num_pairs):
        image1 = lfw_pairs.pairs[pair_index, 0]
        image2 = lfw_pairs.pairs[pair_index, 1]
        grade = lfw_pairs.target[pair_index]

        correct, time_taken, detected_faces = compare_faces(image1, image2, grade, model_name)
        total_time += time_taken
        times.append(time_taken)
        total_faces_detected += detected_faces

        if correct:
            correct_count += 1
        else:
            wrong_count += 1

    accuracy = (correct_count / num_pairs) * 100
    avg_time = total_time / num_pairs
    min_time = min(times)
    max_time = max(times)
    
    return {
        'model_name': model_name,
        'total_pairs': num_pairs,
        'correct': correct_count,
        'wrong': wrong_count,
        'accuracy': accuracy,
        'total_time': total_time,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'total_faces_detected': total_faces_detected
    }

# Wczytanie zbioru danych
lfw_pairs = fetch_lfw_pairs(subset='train')

# Ocena dla obu funkcji
#face_recognition_stats1 = evaluate_model("Face Recognition1", lfw_pairs, 100)
face_recognition_stats2 = evaluate_model("Face Recognition2", lfw_pairs, 100)

# Wyświetlenie wyników
def print_stats(stats):
    print(f"Model: {stats['model_name']}")
    print(f"Łączna liczba par: {stats['total_pairs']}")
    print(f"Poprawnie przeanalizowane: {stats['correct']}")
    print(f"Błędnie przeanalizowane: {stats['wrong']}")
    print(f"Dokładność: {stats['accuracy']:.2f}%")
    print(f"Całkowity czas analizy: {stats['total_time']:.2f} sekund")
    print(f"Średni czas analizy: {stats['avg_time']:.2f} sekund")
    print(f"Najkrótszy czas analizy: {stats['min_time']:.2f} sekund")
    print(f"Najdłuższy czas analizy: {stats['max_time']:.2f} sekund")
    print(f"Liczba wykrytych twarzy: {stats['total_faces_detected']} z {stats['total_pairs']*2}")
    print("===========================")

#print_stats(face_recognition_stats1)
print_stats(face_recognition_stats2)