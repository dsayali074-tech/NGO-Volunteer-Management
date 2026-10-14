
from database import get_connection
from volunteer.events import (
    view_events,
    register_for_event,
    view_my_registered_events
)
from volunteer.activities import view_my_activities


def volunteer_dashboard(volunteer_id):
    while True:
        print("\n========================================")
        print("         VOLUNTEER DASHBOARD")
        print("========================================")
        print("1. My Profile")
        print("2. View Events")
        print("3. My Activities")
        print("4. Register for Event")
        print("5. My Registered Events")
        print("6. Logout")
        choice = input("Enter your choice: ").strip()

        
        if choice == "1":
            view_profile(volunteer_id)

        elif choice == "2":
            view_events()

        elif choice == "3":
            view_my_activities(volunteer_id)

        elif choice == "4":
            register_for_event(volunteer_id)

        elif choice == "5":
            view_my_registered_events(volunteer_id)

        elif choice == "6":
            print("\nLogged out successfully!")
            break

        else:
            print("\nInvalid choice! Please try again.")



def view_profile(volunteer_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT volunteer_id, name, email, phone, address, skills
            FROM volunteers
            WHERE volunteer_id = %s
        """

        cursor.execute(query, (volunteer_id,))
        volunteer = cursor.fetchone()

        print("\n========== MY PROFILE ==========")

        if volunteer:
            print("Volunteer ID:", volunteer[0])
            print("Name:", volunteer[1])
            print("Email:", volunteer[2])
            print("Phone:", volunteer[3])
            print("Address:", volunteer[4])
            print("Skills:", volunteer[5])
        else:
            print("Volunteer profile not found.")

    except Exception as error:
        print("Error fetching profile:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()
