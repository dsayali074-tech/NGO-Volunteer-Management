
from database import get_connection


def activity_management():
    while True:
        print("\n================================")
        print("       ACTIVITY MANAGEMENT")
        print("================================")
        print("1. View All Activities")
        print("2. Add New Activity")
        print("3. Assign Activity to Volunteer")
        print("4. Back to Admin Dashboard")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_activities()
        elif choice == "2":
            add_activity()
        elif choice == "3":
            assign_activity()
        elif choice == "4":
            break
        else:
            print("Invalid choice! Please try again.")


def view_activities():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT activity_id, event_id, activity_name,
                   description, status
            FROM activities
        """)

        activities = cursor.fetchall()

        print("\n========== ALL ACTIVITIES ==========")

        if not activities:
            print("No activities found.")
        else:
            for activity in activities:
                print(activity)

    except Exception as error:
        print("Error viewing activities:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def add_activity():
    print("\n========== ADD NEW ACTIVITY ==========")

    event_id = input("Enter Event ID: ").strip()
    activity_name = input("Enter activity name: ").strip()
    description = input("Enter activity description: ").strip()

    if not event_id or not activity_name:
        print("Event ID and activity name are required.")
        return

    connection = None
    cursor = None

    try:
        event_id = int(event_id)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT event_id FROM events WHERE event_id = %s",
            (event_id,)
        )

        if cursor.fetchone() is None:
            print("Event ID does not exist.")
            return

        cursor.execute("""
            INSERT INTO activities
            (event_id, activity_name, description, status)
            VALUES (%s, %s, %s, %s)
        """, (event_id, activity_name, description, "Pending"))

        connection.commit()

        print("\nActivity added successfully!")
        print("New Activity ID:", cursor.lastrowid)

    except ValueError:
        print("Event ID must be a number.")

    except Exception as error:
        if connection:
            connection.rollback()
        print("Error adding activity:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def assign_activity():
    print("\n========== ASSIGN ACTIVITY TO VOLUNTEER ==========")

    activity_id = input("Enter Activity ID: ").strip()
    volunteer_id = input("Enter Volunteer ID: ").strip()

    if not activity_id or not volunteer_id:
        print("Activity ID and Volunteer ID are required.")
        return

    connection = None
    cursor = None

    try:
        activity_id = int(activity_id)
        volunteer_id = int(volunteer_id)

        connection = get_connection()
        cursor = connection.cursor()

        # Check activity
        cursor.execute(
            "SELECT activity_id FROM activities WHERE activity_id = %s",
            (activity_id,)
        )

        if cursor.fetchone() is None:
            print("Activity ID does not exist.")
            return

        # Check volunteer
        cursor.execute(
            "SELECT volunteer_id FROM volunteers WHERE volunteer_id = %s",
            (volunteer_id,)
        )

        if cursor.fetchone() is None:
            print("Volunteer ID does not exist.")
            return

        # Check duplicate assignment
        cursor.execute("""
            SELECT activity_volunteer_id
            FROM activity_volunteers
            WHERE activity_id = %s AND volunteer_id = %s
        """, (activity_id, volunteer_id))

        if cursor.fetchone() is not None:
            print("This activity is already assigned to this volunteer.")
            return

        # Insert assignment
        cursor.execute("""
            INSERT INTO activity_volunteers
            (activity_id, volunteer_id, assigned_date, status)
            VALUES (%s, %s, CURDATE(), %s)
        """, (activity_id, volunteer_id, "Assigned"))

        connection.commit()

        print("\nActivity assigned successfully!")
        print("Activity ID:", activity_id)
        print("Volunteer ID:", volunteer_id)

    except ValueError:
        print("Activity ID and Volunteer ID must be numbers.")

    except Exception as error:
        if connection:
            connection.rollback()
        print("Error assigning activity:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
