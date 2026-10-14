
from database import get_connection


# 1. VIEW ALL VOLUNTEERS
def view_volunteers():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT volunteer_id, name, email, phone, address, skills
            FROM volunteers
            ORDER BY volunteer_id
        """

        cursor.execute(query)
        volunteers = cursor.fetchall()

        print("\n========== ALL VOLUNTEERS ==========")

        if not volunteers:
            print("No volunteers found.")
        else:
            for volunteer in volunteers:
                print("-" * 40)
                print("Volunteer ID:", volunteer[0])
                print("Name:", volunteer[1])
                print("Email:", volunteer[2])
                print("Phone:", volunteer[3])
                print("Address:", volunteer[4])
                print("Skills:", volunteer[5])

    except Exception as error:
        print("Error fetching volunteers:", error)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


# 2. ADD NEW VOLUNTEER
def add_volunteer():
    print("\n========== ADD NEW VOLUNTEER ==========")

    name = input("Enter volunteer name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone: ").strip()
    password = input("Create volunteer password: ").strip()
    address = input("Enter address: ").strip()
    skills = input("Enter skills: ").strip()

    if not all([name, email, phone, password, address, skills]):
        print("All fields are required!")
        return

    if "@" not in email or "." not in email:
        print("Please enter a valid email address.")
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

        print("\nVolunteer added successfully!")
        print("New Volunteer ID:", cursor.lastrowid)

    except Exception as error:
        if connection is not None:
            connection.rollback()
        print("Error adding volunteer:", error)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


# 3. UPDATE VOLUNTEER
def update_volunteer():
    print("\n========== UPDATE VOLUNTEER ==========")

    volunteer_id = input("Enter Volunteer ID to update: ").strip()

    if not volunteer_id.isdigit():
        print("Please enter a valid numeric Volunteer ID.")
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT volunteer_id, name, email, phone, address, skills
            FROM volunteers
            WHERE volunteer_id = %s
            """,
            (int(volunteer_id),)
        )

        volunteer = cursor.fetchone()

        if volunteer is None:
            print("Volunteer not found!")
            return

        print("\nCurrent Volunteer Details:")
        print("Name:", volunteer[1])
        print("Email:", volunteer[2])
        print("Phone:", volunteer[3])
        print("Address:", volunteer[4])
        print("Skills:", volunteer[5])

        print("\nLeave a field blank to keep its current value.")

        name = input(f"Name [{volunteer[1]}]: ").strip()
        email = input(f"Email [{volunteer[2]}]: ").strip()
        phone = input(f"Phone [{volunteer[3]}]: ").strip()
        address = input(f"Address [{volunteer[4]}]: ").strip()
        skills = input(f"Skills [{volunteer[5]}]: ").strip()

        name = name or volunteer[1]
        email = email or volunteer[2]
        phone = phone or volunteer[3]
        address = address or volunteer[4]
        skills = skills or volunteer[5]

        if "@" not in email or "." not in email:
            print("Please enter a valid email address.")
            return

        cursor.execute(
            """
            UPDATE volunteers
            SET name = %s,
                email = %s,
                phone = %s,
                address = %s,
                skills = %s
            WHERE volunteer_id = %s
            """,
            (
                name,
                email,
                phone,
                address,
                skills,
                int(volunteer_id)
            )
        )

        connection.commit()
        print("\nVolunteer updated successfully!")

    except Exception as error:
        if connection is not None:
            connection.rollback()
        print("Error updating volunteer:", error)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


# 4. VOLUNTEER MANAGEMENT MENU
def volunteer_management():
    while True:
        print("\n========== VOLUNTEER MANAGEMENT ==========")
        print("1. View All Volunteers")
        print("2. Add Volunteer")
        print("3. Update Volunteer")
        print("4. Back to Admin Dashboard")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_volunteers()

        elif choice == "2":
            add_volunteer()

        elif choice == "3":
            update_volunteer()

        elif choice == "4":
            print("Returning to Admin Dashboard...")
            break

        else:
            print("Invalid choice! Please try again.")
