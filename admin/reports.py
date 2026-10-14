from database import get_connection


def view_reports():
    while True:
        print("\n================================")
        print("          ADMIN REPORTS")
        print("================================")
        print("1. Total Volunteers")
        print("2. Total Events")
        print("3. Total Donations")
        print("4. Total Event Registrations")
        print("5. Total Donation Amount")
        print("6. Back to Admin Dashboard")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_count("volunteers", "Total Volunteers")

        elif choice == "2":
            show_count("events", "Total Events")

        elif choice == "3":
            show_count("donations", "Total Donations")

        elif choice == "4":
            show_count(
                "event_registrations",
                "Total Event Registrations"
            )

        elif choice == "5":
            show_total_donation_amount()

        elif choice == "6":
            print("Returning to Admin Dashboard...")
            break

        else:
            print("Invalid choice! Please try again.")


def show_count(table_name, label):
    connection = None
    cursor = None

    allowed_tables = [
        "volunteers",
        "events",
        "donations",
        "event_registrations"
    ]

    if table_name not in allowed_tables:
        print("Invalid table name.")
        return

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT COUNT(*) FROM `{table_name}`"
        )

        result = cursor.fetchone()

        print(f"\n{label}: {result[0]}")

    except Exception as error:
        print("Error generating report:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def show_total_donation_amount():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM donations
        """)

        result = cursor.fetchone()

        total_amount = result[0]

        print("\n========== TOTAL DONATION AMOUNT ==========")
        print(f"Total Donation Amount: ₹{total_amount:.2f}")

    except Exception as error:
        print("Error calculating donation amount:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()