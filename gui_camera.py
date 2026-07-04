import PySimpleGUI as sg
import cv2
import os
import apka as ap
import json
from datetime import datetime, timedelta
import numpy as np
import html_handling as hh
import webbrowser

def take_picture(frame):
    filename = "picture.jpg"
    cv2.imwrite(filename, frame)
    
    trimmed_faces = ap.prepare_image(filename)
    
    if trimmed_faces is None:
        delete_picture(filename)
    else:
        sg.popup("Zdjęcie zapisane i przetworzone.")

def delete_picture(picture_name):
    if os.path.exists(picture_name):
        os.remove(picture_name)

def list_cameras():
    index = 0
    available_cameras = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        available_cameras.append(index)
        cap.release()
        index += 1
    return available_cameras

def select_camera():
    cameras = list_cameras()
    if not cameras:
        sg.popup_error("Nie znaleziono dostępnych kamer")
        return None
    elif len(cameras) == 1:
        return cameras[0]
    else:
        camera_index = sg.popup_get_text(f"Wybierz kamerę (0-{len(cameras)-1}):", "Wybór kamery")
        if camera_index is None or not camera_index.isdigit() or int(camera_index) not in cameras:
            sg.popup_error("Nieprawidłowy wybór kamery")
            return None
        return int(camera_index)

def get_work_duration(start_time, end_time):
    start_dt = datetime.strptime(start_time, "%H:%M")
    end_dt = datetime.strptime(end_time, "%H:%M")
    work_duration = end_dt - start_dt
    hours = work_duration.seconds // 3600
    minutes = (work_duration.seconds // 60) % 60
    return hours, minutes

def show_statistics(first_name, last_name, department, period):
    try:
        with open("obecnosc.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        total_hours = 0
        total_minutes = 0
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)

        for employee in data["employees"]:
            if (employee.get("first_name") == first_name and
                employee.get("last_name") == last_name and
                employee.get("department") == department):

                for attendance in employee.get("attendance", []):
                    attendance_date = datetime.strptime(attendance.get("date"), "%Y-%m-%d")

                    if period == 'today' and attendance_date.date() == today.date():
                        for entry in attendance.get("entries", []):
                            if entry["type"] == "entry":
                                start_time = entry["time"]
                            if entry["type"] == "exit":
                                end_time = entry["time"]
                                hours, minutes = get_work_duration(start_time, end_time)
                                total_hours += hours
                                total_minutes += minutes

                    elif period == 'week' and attendance_date >= start_of_week:
                        for entry in attendance.get("entries", []):
                            if entry["type"] == "entry":
                                start_time = entry["time"]
                            if entry["type"] == "exit":
                                end_time = entry["time"]
                                hours, minutes = get_work_duration(start_time, end_time)
                                total_hours += hours
                                total_minutes += minutes

                    elif period == 'month' and attendance_date >= start_of_month:
                        for entry in attendance.get("entries", []):
                            if entry["type"] == "entry":
                                start_time = entry["time"]
                            if entry["type"] == "exit":
                                end_time = entry["time"]
                                hours, minutes = get_work_duration(start_time, end_time)
                                total_hours += hours
                                total_minutes += minutes

                total_hours += total_minutes // 60
                total_minutes = total_minutes % 60
                total_time = f"{total_hours}h {total_minutes}m"
                
                return total_time

        raise ValueError("Nie znaleziono użytkownika o podanych danych.")

    except FileNotFoundError:
        print("Nie znaleziono pliku obecnosc.json!")
        return False
    except ValueError as e:
        print(str(e))
        return False

def show_statistics_all():
    try:
        with open("obecnosc.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        general_table_html = hh.generate_html_table(data)
        
        individual_tables_html = hh.generate_individual_tables(data)
        
        full_html_content = general_table_html + individual_tables_html
        
        html_file = "attendance_report.html"
        with open(html_file, "w", encoding="utf-8") as output_file:
            output_file.write(full_html_content)

        print("HTML file 'attendance_report.html' generated successfully.")
        webbrowser.open(html_file)
        
    except FileNotFoundError:
        print("Nie znaleziono pliku obecnosc.json!")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def write_to_json_attendance(first_name, last_name, department, current_date, current_time, status):
    try:
        with open("obecnosc.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for employee in data["employees"]:
            if (employee.get("first_name") == first_name and
                employee.get("last_name") == last_name and
                employee.get("department") == department):
                
                for attendance in employee.get("attendance", []):
                    if attendance["date"] == current_date:
                        attendance["entries"].append({
                            "type": status,
                            "time": current_time
                        })
                        break
                else:
                    employee.setdefault("attendance", []).append({
                        "date": current_date,
                        "entries": [
                            {
                                "type": status,
                                "time": current_time
                            }
                        ]
                    })
                break
        else:
            raise ValueError("Nie znaleziono użytkownika o podanych danych.")

        with open("obecnosc.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print("Zaktualizowano obecność dla użytkownika.")
        return True

    except FileNotFoundError:
        print("Nie znaleziono pliku obecnosc.json!")
        return False
    except ValueError as e:
        print(str(e))
        return False

def write_to_json_register(first_name, last_name, department, password, encoding):
    try:
        try:
            with open("dane_logowania.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        new_user = {
            "first_name": first_name,
            "last_name": last_name,
            "department": department,
            "password": password
        }
        
        if encoding is not None:
            encoding = encoding.tolist() if hasattr(encoding, 'tolist') else encoding
            new_user["encoding"] = encoding

        data.append(new_user)

        with open("dane_logowania.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print("Dodano użytkownika.")
        write_to_json_register_attendance(first_name, last_name, department)
        return True

    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")
        return False

def write_to_json_register_attendance(first_name, last_name, department):
    try:
        try:
            with open("obecnosc.json", "r", encoding="utf-8") as file:
                attendance_data = json.load(file)
        except FileNotFoundError:
            attendance_data = {"employees": []}

        new_attendance_user = {
            "first_name": first_name,
            "last_name": last_name,
            "department": department,
            "attendance": []
        }

        attendance_data["employees"].append(new_attendance_user)

        with open("obecnosc.json", "w", encoding="utf-8") as file:
            json.dump(attendance_data, file, indent=4, ensure_ascii=False)

        print("Dodano użytkownika do obecnosc.json.")
    
    except Exception as e:
        print(f"Wystąpił błąd przy dodawaniu użytkownika do obecnosc.json: {str(e)}")

def get_encoding_from_json(first_name, last_name, department, json_file="dane_logowania.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        for user in data:
            if (
                user["first_name"] == first_name and
                user["last_name"] == last_name and
                user["department"] == department and
                "encoding" in user
            ):
                encoding = np.array(user["encoding"])
                return encoding

        print("Użytkownik nie znaleziony lub brak kodowania.")
        return None

    except FileNotFoundError:
        print("Plik JSON nie istnieje.")
        return None
    except Exception as e:
        print(f"Błąd podczas odczytu kodowania z JSON: {e}")
        return None

def camera_view():
    camera_index = select_camera()
    if camera_index is None:
        return None

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        sg.popup_error(f"Nie można uruchomić kamery {camera_index}")
        return None

    layout_camera = [
        [sg.Image(filename="", key="image")],
        [sg.Column(
            [[sg.Button("Zrób zdjęcie", size=(15, 2)), sg.Button("Cofnij", size=(15, 2))]],
            justification='center',
            element_justification='center'
        )]
    ]
    window_camera = sg.Window(f"Podgląd kamery {camera_index}", layout_camera, location=(100, 100))

    circle_color = (255, 255, 255)
    alpha = 0.5
    thickness = 2
    ellipse_size = (150, 200)

    while True:
        event, values = window_camera.read(timeout=20)
        ret, frame = cap.read()
        if not ret:
            sg.popup_error("Błąd podczas odczytu obrazu z kamery")
            break

        overlay = frame.copy()
        height, width, _ = frame.shape
        center = (width // 2, height // 2)
        cv2.ellipse(overlay, center, ellipse_size, 0, 0, 360, circle_color, thickness)

        frame_with_circle = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        imgbytes = cv2.imencode(".png", frame_with_circle)[1].tobytes()
        window_camera["image"].update(data=imgbytes)

        if event == "Zrób zdjęcie":
            take_picture(frame)
            face_encoding = ap.encode_face('picture.jpg')
            cap.release()
            window_camera.close()
            return True, face_encoding
        elif event in (sg.WINDOW_CLOSED, "Cofnij"):
            break

    cap.release()
    window_camera.close()