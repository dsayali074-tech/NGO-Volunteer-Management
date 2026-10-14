
from database import get_connection


def volunteer_registration():
    print("\n========== VOLUNTEER REGISTRATION ==========")

    name = input("Enter your full name: ").strip()
    email = input("Enter your email: ").strip()
    phone = input("Enter your phone number: ").strip()
    password = input("Create your password: ").strip()
    address = input("Enter your address: ").strip()
    skills = input("Enter your skills: ").strip()

    # Validate input
    if not all([name, email, phone, password, address, skills]):
        print("\nAll fields are required!")
        return

    if "@" not in email or "." not in email:
        print("\nPlease enter a valid email address.")
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO volunteers
            (name, email, phone, password, address, skills)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (name, email, phone, password, address, skills)

        cursor.execute(query, values)
        connection.commit()

        print("\nRegistration successful!")
        print("Your Volunteer ID:", cursor.lastrowid)
        print("You can now log in using your email and password.")

    except Exception as error:
        if connection is not None:
            connection.rollback()

        print("\nRegistration failed:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()
