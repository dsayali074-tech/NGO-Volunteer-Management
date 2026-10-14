
from auth.admin_login import admin_login
from auth.volunteer_auth import volunteer_login
from volunteer.registration import volunteer_registration


def main_menu():
    while True:
        print("\n========================================")
        print("     NGO VOLUNTEER MANAGEMENT SYSTEM")
        print("========================================")
        print("1. Admin Login")
        print("2. Volunteer Register")
        print("3. Volunteer Login")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            admin_login()

        elif choice == "2":
            volunteer_registration()
        
        elif choice == "3":
            volunteer_login()

        elif choice == "4":
            print("\nThank you for using NGO Volunteer Management System!")
            break

        else:
            print("\nInvalid choice! Please try again.")


if __name__ == "__main__":
    main_menu()
