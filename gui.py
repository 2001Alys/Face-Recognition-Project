import PySimpleGUI as sg
import gui_camera as gc
import json
from datetime import datetime
import apka as ap

def check_user(first_name, last_name, department):
    try:
        with open("dane_logowania.json", "r", encoding="utf-8") as file:
            users = json.load(file)
    except FileNotFoundError:
        sg.popup_error("Nie znaleziono pliku dane.json!")
        return False

    for user in users:
        if (user["first_name"] == first_name and 
            user["last_name"] == last_name and 
            user["department"] == department):
            return True
    return False

def verify_user(first_name, last_name, department, password):
    try:
        with open("dane_logowania.json", "r", encoding="utf-8") as file:
            users = json.load(file)
    except FileNotFoundError:
        sg.popup_error("Nie znaleziono pliku dane.json!")
        return False

    for user in users:
        if (user["first_name"] == first_name and 
            user["last_name"] == last_name and 
            user["department"] == department and 
            user["password"] == password):
            return True
    return False

def verify_face(first_name, last_name, department):
    try:
        status, encoding = gc.camera_view()

        if not status:
            print("Nie udało się uzyskać kodowania z kamery.")
            return False

        encoding_json = gc.get_encoding_from_json(first_name, last_name, department)

        if encoding_json is None:
            print("Nie znaleziono odpowiedniego kodowania w JSON.")
            return False

        results = ap.compare_faces_face_recognition(encoding, encoding_json)
        return results

    except Exception as e:
        print(f"Błąd w weryfikacji twarzy: {e}")
        return False

def show_dashboard(first_name, last_name, department):
    
    if department == 'Prezes':
        layout_dashboard = [
            [sg.Column(
                [[sg.Text(f"{last_name} {first_name} - {department}", font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Przyjście", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Wyjście", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Statystyki", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Statystyki Wszystkich", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Wyloguj", size=(20, 2), font=("Helvetica", 12))]],
                element_justification='center',
                vertical_alignment='center',
                justification='center'
            )]
        ]
        height = 360
    elif department == 'Technik':
        layout_dashboard = [
            [sg.Column(
                [[sg.Text(f"{last_name} {first_name} - {department}", font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Przyjście", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Wyjście", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Statystyki", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Statystyki Wszystkich", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Zarejestruj", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Wyloguj", size=(20, 2), font=("Helvetica", 12))]],
                element_justification='center',
                vertical_alignment='center',
                justification='center'
            )]
        ]
        height = 420
    elif department == 'Pracownik':
        layout_dashboard = [
            [sg.Column(
                [[sg.Text(f"{last_name} {first_name} - {department}", font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Przyjście", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Wyjście", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Statystyki", size=(20, 2), font=("Helvetica", 12))],
                 [sg.VPush()],
                 [sg.Button("Wyloguj", size=(20, 2), font=("Helvetica", 12))]],
                element_justification='center',
                vertical_alignment='center',
                justification='center'
            )]
        ]
        height = 300
    
    window_dashboard = sg.Window("App", layout_dashboard, location=(600, 400), size=(300, height))

    while True:
        event, _ = window_dashboard.read()

        if event == "Wyloguj" or event == sg.WINDOW_CLOSED:
            window_dashboard.close()
            break

        elif event == "Przyjście":
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M")
            gc.write_to_json_attendance(first_name, last_name, department, current_date, current_time, "entry")
            sg.popup("Przyjście zostało odnotowane.")
        elif event == "Wyjście":
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M")
            gc.write_to_json_attendance(first_name, last_name, department, current_date, current_time, "exit")
            sg.popup("Wyjście zostało odnotowane.")
        elif event == "Statystyki":
            attendance_today = gc.show_statistics(first_name, last_name, department, 'today')
            attendance_week = gc.show_statistics(first_name, last_name, department, 'week')
            attendance_month = gc.show_statistics(first_name, last_name, department, 'month')
            sg.popup(f"Dzisiaj: {attendance_today}, Tydzień: {attendance_week}, Mieisąc: {attendance_month}.")
        elif event == "Statystyki Wszystkich":
            gc.show_statistics_all()
        elif event == "Zarejestruj":
            window_dashboard.close()
            register_window()

    main_window()

def register_window():
    layout_main = [
        [sg.Column(
            [[sg.Text("ZAREJESTRUJ", font=("Helvetica", 20))],
             [sg.VPush()],
             [sg.Text("Imię:", font=("Helvetica", 14)), sg.InputText(key="first_name", font=("Helvetica", 14), size=(20, 1))],
             [sg.VPush()],
             [sg.Text("Nazwisko:", font=("Helvetica", 14)), sg.InputText(key="last_name", font=("Helvetica", 14), size=(20, 1))],
             [sg.VPush()],
             [sg.Text("Dział:", font=("Helvetica", 14)), sg.Combo(
                ['Prezes', 'Pracownik', 'Technik'], key="department", default_value='Pracownik', font=("Helvetica", 14), size=(13, 1), readonly=True)],
             [sg.VPush()],
             [sg.Text("Hasło:", font=("Helvetica", 14)), sg.InputText(key="password", font=("Helvetica", 14), size=(20, 1), password_char='*')],
             [sg.VPush()],
             [sg.Button("Załóż konto", size=(23, 2), font=("Helvetica", 14))]],
            element_justification='center',
            vertical_alignment='center',
            justification='center'
        )]
    ]
    
    reg_main = sg.Window("App", layout_main, location=(600, 400), size=(330, 290))

    while True:
        event, values = reg_main.read()
        if event in (sg.WINDOW_CLOSED,):
            break
        elif event in ("Załóż konto"):
            first_name = values["first_name"].strip()
            last_name = values["last_name"].strip()
            department = values["department"].strip()
            password = values["password"].strip()
            
            if not first_name or not last_name or not department or not password:
                sg.popup_error("Wszystkie pola muszą zostać uzupełnione!")
                reg_main.close()
                register_window()
            if verify_user(first_name, last_name, department, password):
                sg.popup_error("Osoba już istnieje!")
                reg_main["first_name"].update("")
                reg_main["last_name"].update("")
                reg_main["password"].update("")
            elif not verify_user(first_name, last_name, department, password):
                reg_main.close()
                status, encoding = gc.camera_view()
                gc.write_to_json_register(first_name, last_name, department, password, encoding)
                sg.popup("Osoba została dodana.")
                main_window()

    reg_main.close()
    
def login_window(first_name, last_name, department):
    layout_main = [
        [sg.Column(
            [[sg.Text("Hasło:", font=("Helvetica", 14)), sg.InputText(key="password", font=("Helvetica", 14), size=(20, 1), password_char='*')],
             [sg.VPush()],
             [sg.Button("Zweryfikuj hasło", size=(23, 2), font=("Helvetica", 14))],
             [sg.Text("Lub:", font=("Helvetica", 14))],
             [sg.VPush()],
             [sg.Button("Zweryfikuj twarz", size=(23, 2), font=("Helvetica", 14))],
             [sg.VPush()],
             [sg.Button("Cofnij", size=(23, 2), font=("Helvetica", 14))]],
            element_justification='center',
            vertical_alignment='center',
            justification='center'
        )]
    ]
    
    log_window = sg.Window("App", layout_main, location=(600, 400), size=(330, 300))

    while True:
        event, values = log_window.read()
        if event in (sg.WINDOW_CLOSED, "Cofnij"):
            log_window.close()
            break
        
        elif event in ("Zweryfikuj hasło"):
            password = values["password"]
            
            if not verify_user(first_name, last_name, department, password):
                sg.popup_error("Hasło nie zgadza się!")
                log_window["password"].update("")
            elif verify_user(first_name, last_name, department, password):
                log_window.close()
                show_dashboard(first_name, last_name, department)
                
        elif event in ("Zweryfikuj twarz"):
            face_verified = verify_face(first_name, last_name, department)
            if face_verified == False:
                sg.popup_error("Nie rozpoznano osoby.")
                log_window["password"].update("")
            elif face_verified == True:
                log_window.close()
                show_dashboard(first_name, last_name, department)
            elif verify_user(first_name, last_name, department, password):
                log_window.close()
                show_dashboard(first_name, last_name, department)
                
    main_window()
    
def main_window():
    layout_main = [
        [sg.Column(
            [[sg.Text("ZALOGUJ", font=("Helvetica", 20))],
             [sg.VPush()],
             [sg.Text("Imię:", font=("Helvetica", 14)), sg.InputText(key="first_name", font=("Helvetica", 14), size=(20, 1))],
              [sg.VPush()],
             [sg.Text("Nazwisko:", font=("Helvetica", 14)), sg.InputText(key="last_name", font=("Helvetica", 14), size=(20, 1))],
             [sg.VPush()],
             [sg.Text("Dział:", font=("Helvetica", 14)), sg.Combo(
                ['Prezes', 'Pracownik', 'Technik'], key="department", default_value='Pracownik', font=("Helvetica", 14), size=(13, 1), readonly=True)],
             [sg.VPush()],
             [sg.Button("Zweryfikuj", size=(23, 2), font=("Helvetica", 14))]],
            element_justification='center',
            vertical_alignment='center',
            justification='center'
        )]
    ]
    
    window_main = sg.Window("App", layout_main, location=(600, 400), size=(330, 250))

    while True:
        event, values = window_main.read()
        if event in (sg.WINDOW_CLOSED,):
            break
        elif event in ("Zweryfikuj"):
            first_name = values["first_name"]
            last_name = values["last_name"]
            department = values["department"]
            
            if not check_user(first_name, last_name, department):
                sg.popup_error("Nie znaleziono takiego użytkownika.")
                window_main["first_name"].update("")
                window_main["last_name"].update("")
            elif check_user(first_name, last_name, department):
                window_main.close()
                login_window(first_name, last_name, department)

    window_main.close()
    
if __name__ == "__main__":
    gc.delete_picture("picture.jpg")
    main_window()