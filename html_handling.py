from datetime import datetime, timedelta
import gui_camera as gc

def generate_html_table(data):

    html = """
    <html>
    <head>
        <title>Lista Obecnosci</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <h2>Lista Obecnosci</h2>
        <table>
            <tr>
                <th>Nazwisko</th>
                <th>Imię</th>
                <th>Dział</th>
                <th>Dzień</th>
                <th>Tydzień</th>
                <th>Miesiąc</th>
            </tr>
    """

    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    for employee in data["employees"]:
        last_name = employee.get("last_name")
        first_name = employee.get("first_name")
        department = employee.get("department")


        total_day_hours = total_day_minutes = 0
        total_week_hours = total_week_minutes = 0
        total_month_hours = total_month_minutes = 0

        for attendance in employee.get("attendance", []):
            attendance_date = datetime.strptime(attendance.get("date"), "%Y-%m-%d")


            for entry in attendance.get("entries", []):
                if entry["type"] == "entry":
                    start_time = entry["time"]
                if entry["type"] == "exit":
                    end_time = entry["time"]
                    hours, minutes = gc.get_work_duration(start_time, end_time)


                    if attendance_date.date() == today.date():
                        total_day_hours += hours
                        total_day_minutes += minutes
                    if attendance_date >= start_of_week:
                        total_week_hours += hours
                        total_week_minutes += minutes
                    if attendance_date >= start_of_month:
                        total_month_hours += hours
                        total_month_minutes += minutes


        total_day_hours += total_day_minutes // 60
        total_day_minutes = total_day_minutes % 60
        total_week_hours += total_week_minutes // 60
        total_week_minutes = total_week_minutes % 60
        total_month_hours += total_month_minutes // 60
        total_month_minutes = total_month_minutes % 60


        day_total_time = f"{total_day_hours}h {total_day_minutes}m"
        week_total_time = f"{total_week_hours}h {total_week_minutes}m"
        month_total_time = f"{total_month_hours}h {total_month_minutes}m"


        html += f"""
            <tr>
                <td>{last_name}</td>
                <td>{first_name}</td>
                <td>{department}</td>
                <td>{day_total_time}</td>
                <td>{week_total_time}</td>
                <td>{month_total_time}</td>
            </tr>
        """


    html += """
        </table>
    </body>
    </html>
    """

    return html

def generate_individual_tables(data):
    html = """
    <html>
    <head>
        <title>Szczegółowa Lista Obecnosci</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
            .section-title {
                font-size: 20px;
                margin-top: 30px;
            }
        </style>
    </head>
    <body>
        <h2>Szczegółowa Lista Obecnosci</h2>
    """

    categories = ["Prezes", "Pracownik", "Technik"]

    for category in categories:
        employees = [emp for emp in data["employees"] if emp["department"] == category]

        if employees:
            html += f"<h3 class='section-title'>{category}</h3>"

        for employee in employees:
            first_name = employee.get("first_name")
            last_name = employee.get("last_name")

            html += f"""
            <table>
                <tr>
                    <th colspan='3'>Dane: {first_name} {last_name}</th>
                    <th colspan='2'>Dział: {category}</th>
                </tr>
                <tr>
                    <th>Data</th>
                    <th>Wejscie</th>
                    <th>Wyjscie</th>
                    <th>Suma</th>
                </tr>
            """

            attendance_records = sorted(employee.get("attendance", []), key=lambda x: x["date"], reverse=True)

            for attendance in attendance_records:
                date = attendance.get("date")
                entries = attendance.get("entries", [])
                total_hours, total_minutes = 0, 0

                html += f"<tr><td rowspan='{len(entries)//2 + 1}'>{datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')}</td>"

                for i in range(0, len(entries), 2):
                    if i < len(entries) - 1 and entries[i]["type"] == "entry" and entries[i+1]["type"] == "exit":
                        start_time = entries[i]["time"]
                        end_time = entries[i+1]["time"]
                        hours, minutes = gc.get_work_duration(start_time, end_time)
                        total_hours += hours
                        total_minutes += minutes

                        html += f"<td>{start_time}</td><td>{end_time}</td><td>{hours}h {minutes}m</td></tr><tr>"

                total_hours += total_minutes // 60
                total_minutes = total_minutes % 60
                html += f"<tr><td colspan='3'><strong>Suma:</strong></td><td><strong>{total_hours}h {total_minutes}m</strong></td></tr>"

            html += "</table>"

    html += "</body></html>"

    return html