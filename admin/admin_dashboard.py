
from admin.volunteer_management import volunteer_management
from admin.event_management import event_management
from admin.activity_management import activity_management
from admin.donation_management import donation_management
from admin.reports import view_reports
from admin.attendance_management import attendance_management


def admin_dashboard():
    while True:
        print("\n========================================")
        print("             ADMIN DASHBOARD")
        print("========================================")
        print("1. Manage Volunteers")
        print("2. Manage Events")
        print("3. Manage Activities")
        print("4. Manage Donations")
        print("5. View Reports")
        print("6. Logout")
        print("7. Manage Attendance")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            volunteer_management()

        elif choice == "2":
            event_management()

        elif choice == "3":
            activity_management()

        elif choice == "4":
            donation_management()

        elif choice == "5":
            view_reports()

        elif choice == "6":
            print("Admin logged out successfully!")
            break
        elif choice == "7":
           attendance_management()

        else:
            print("Invalid choice! Please try again.")
