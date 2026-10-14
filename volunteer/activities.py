
from database import get_connection


def view_my_activities(volunteer_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT a.activity_id,
                   a.activity_name,
                   a.description,
                   av.status
            FROM activities a
            JOIN activity_volunteers av
                ON a.activity_id = av.activity_id
            WHERE av.volunteer_id = %s
        """

        cursor.execute(query, (volunteer_id,))
        activities = cursor.fetchall()

        print("\n========== MY ACTIVITIES ==========")

        if not activities:
            print("No activities assigned to you yet.")
            return

        for activity in activities:
            print("\n" + "-" * 35)
            print("Activity ID:", activity[0])
            print("Activity Name:", activity[1])
            print("Description:", activity[2])
            print("Status:", activity[3])

        print("\n1. Update Activity Status")
        print("2. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            update_activity_status(volunteer_id)
        elif choice == "2":
            return
        else:
            print("Invalid choice!")

    except Exception as error:
        print("Error fetching activities:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def update_activity_status(volunteer_id):
    connection = None
    cursor = None

    try:
        activity_id = input("Enter Activity ID: ").strip()

        if not activity_id:
            print("Activity ID is required.")
            return

        activity_id = int(activity_id)

        print("\nSelect New Status:")
        print("1. Assigned")
        print("2. In Progress")
        print("3. Completed")

        status_choice = input("Enter your choice: ").strip()

        status_options = {
            "1": "Assigned",
            "2": "In Progress",
            "3": "Completed"
        }

        if status_choice not in status_options:
            print("Invalid status choice!")
            return

        new_status = status_options[status_choice]

        connection = get_connection()
        cursor = connection.cursor()

        # Confirm this activity is assigned to this volunteer
        cursor.execute(
            """
            SELECT activity_volunteer_id
            FROM activity_volunteers
            WHERE activity_id = %s
              AND volunteer_id = %s
            """,
            (activity_id, volunteer_id)
        )

        assignment = cursor.fetchone()

        if assignment is None:
            print("This activity is not assigned to you.")
            return

        cursor.execute(
            """
            UPDATE activity_volunteers
            SET status = %s
            WHERE activity_id = %s
              AND volunteer_id = %s
            """,
            (new_status, activity_id, volunteer_id)
        )

        connection.commit()

        print("\nActivity status updated successfully!")
        print("Activity ID:", activity_id)
        print("New Status:", new_status)

    except ValueError:
        print("Activity ID must be a number.")

    except Exception as error:
        if connection is not None:
            connection.rollback()
        print("Error updating activity status:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()
