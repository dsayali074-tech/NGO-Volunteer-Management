
from database import get_connection
from volunteer.dashboard import volunteer_dashboard


def volunteer_login():
    print("\n========== VOLUNTEER LOGIN ==========")

    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    connection = None
    cursor = None
    volunteer = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT volunteer_id, name, email
            FROM volunteers
            WHERE email = %s AND password = %s
        """

        cursor.execute(query, (email, password))
        volunteer = cursor.fetchone()

    except Exception as error:
        print("Login error:", error)
        return

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

    if volunteer:
        print("\nVolunteer login successful!")
        print("Welcome,", volunteer[1])
        print("Volunteer ID:", volunteer[0])

        # Open Volunteer Dashboard
        volunteer_dashboard(volunteer[0])

    else:
        print("\nInvalid email or password!")
