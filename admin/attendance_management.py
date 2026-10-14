
from database import get_connection


def attendance_management():
    while True:
        print("\n================================")
        print("    ATTENDANCE MANAGEMENT")
        print("================================")
        print("1. View All Attendance")
        print("2. Mark Attendance")
        print("3. Back to Admin Dashboard")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_attendance()
        elif choice == "2":
            mark_attendance()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")


def view_attendance():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT attendance_id, event_id, volunteer_id,
                   attendance_date, status
            FROM attendance
            ORDER BY attendance_date DESC
        """)

        records = cursor.fetchall()

        print("\n========== ALL ATTENDANCE ==========")

        if not records:
            print("No attendance records found.")
        else:
            for record in records:
                print(
                    f"Attendance ID: {record[0]} | "
                    f"Event ID: {record[1]} | "
                    f"Volunteer ID: {record[2]} | "
                    f"Date: {record[3]} | "
                    f"Status: {record[4]}"
                )

    except Exception as error:
        print("Error viewing attendance:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def mark_attendance():
    print("\n========== MARK ATTENDANCE ==========")

    event_input = input("Enter Event ID: ").strip()
    volunteer_input = input("Enter Volunteer ID: ").strip()

    if not event_input or not volunteer_input:
        print("Event ID and Volunteer ID are required.")
        return

    connection = None
    cursor = None

    try:
        event_id = int(event_input)
        volunteer_id = int(volunteer_input)

        print("\nSelect Attendance Status:")
        print("1. Present")
        print("2. Absent")

        status_choice = input("Enter your choice: ").strip()

        statuses = {
            "1": "Present",
            "2": "Absent"
        }

        if status_choice not in statuses:
            print("Invalid status choice!")
            return

        status = statuses[status_choice]

        connection = get_connection()
        cursor = connection.cursor()

        # Check whether the event exists
        cursor.execute(
            "SELECT event_id FROM events WHERE event_id = %s",
            (event_id,)
        )

        if cursor.fetchone() is None:
            print("Event ID does not exist.")
            return

        # Check whether the volunteer exists
        cursor.execute(
            "SELECT volunteer_id FROM volunteers WHERE volunteer_id = %s",
            (volunteer_id,)
        )

        if cursor.fetchone() is None:
            print("Volunteer ID does not exist.")
            return

        # Check duplicate attendance for the same event and date
        cursor.execute("""
            SELECT attendance_id
            FROM attendance
            WHERE event_id = %s
              AND volunteer_id = %s
              AND attendance_date = CURDATE()
        """, (event_id, volunteer_id))

        if cursor.fetchone() is not None:
            print("Attendance already marked for this volunteer and event today.")
            return

        # Insert attendance record
        cursor.execute("""
            INSERT INTO attendance
            (event_id, volunteer_id, attendance_date, status)
            VALUES (%s, %s, CURDATE(), %s)
        """, (event_id, volunteer_id, status))

        connection.commit()

        print("\nAttendance marked successfully!")
        print("Event ID:", event_id)
        print("Volunteer ID:", volunteer_id)
        print("Date: Today")
        print("Status:", status)

    except ValueError:
        print("Event ID and Volunteer ID must be numbers.")

    except Exception as error:
        if connection:
            connection.rollback()
        print("Error marking attendance:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
