from database import get_connection
from admin.admin_dashboard import admin_dashboard


def admin_login():

    print("\n========== ADMIN LOGIN ==========")

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT admin_id, username
        FROM admins
        WHERE username = %s AND password = %s
        """

        cursor.execute(query, (username, password))

        admin = cursor.fetchone()

        if admin:
            print("\nLogin successful!")
            print("Welcome Admin!")

            admin_dashboard()

        else:
            print("\nInvalid username or password!")

    except Exception as error:
        print("\nAdmin login error:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()