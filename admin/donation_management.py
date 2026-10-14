from database import get_connection


def donation_management():
    while True:
        print("\n================================")
        print("       DONATION MANAGEMENT")
        print("================================")
        print("1. View All Donations")
        print("2. Add New Donation")
        print("3. Back to Admin Dashboard")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_donations()

        elif choice == "2":
            add_donation()

        elif choice == "3":
            print("Returning to Admin Dashboard...")
            break

        else:
            print("Invalid choice! Please try again.")


def view_donations():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT donation_id,
                   donor_name,
                   donor_email,
                   amount,
                   donation_date
            FROM donations
            ORDER BY donation_id DESC
        """)

        donations = cursor.fetchall()

        print("\n========== ALL DONATIONS ==========")

        if not donations:
            print("No donations found.")
            return

        for donation in donations:
            print("\n----------------------------------------")
            print("Donation ID:", donation[0])
            print("Donor Name:", donation[1])
            print("Donor Email:", donation[2])
            print("Amount:", donation[3])
            print("Donation Date:", donation[4])

    except Exception as error:
        print("Error viewing donations:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def add_donation():
    print("\n========== ADD NEW DONATION ==========")

    donor_name = input("Enter donor name: ").strip()
    donor_email = input("Enter donor email: ").strip()
    amount = input("Enter donation amount: ").strip()
    donation_date = input(
        "Enter donation date (YYYY-MM-DD): "
    ).strip()

    # Required field validation
    if not donor_name:
        print("Donor name is required.")
        return

    if not amount:
        print("Donation amount is required.")
        return

    connection = None
    cursor = None

    try:
        # Convert amount to number
        amount = float(amount)

        if amount <= 0:
            print("Donation amount must be greater than 0.")
            return

        # Email validation
        if donor_email and "@" not in donor_email:
            print("Please enter a valid email address.")
            return

        connection = get_connection()
        cursor = connection.cursor()

        # If date is provided
        if donation_date:

            cursor.execute(
                """
                INSERT INTO donations
                (
                    donor_name,
                    donor_email,
                    amount,
                    donation_date
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    donor_name,
                    donor_email if donor_email else None,
                    amount,
                    donation_date
                )
            )

        # If date is blank, use today's date
        else:

            cursor.execute(
                """
                INSERT INTO donations
                (
                    donor_name,
                    donor_email,
                    amount,
                    donation_date
                )
                VALUES (%s, %s, %s, CURDATE())
                """,
                (
                    donor_name,
                    donor_email if donor_email else None,
                    amount
                )
            )

        connection.commit()

        print("\nDonation added successfully!")
        print("New Donation ID:", cursor.lastrowid)

    except ValueError:
        print("Donation amount must be a valid number.")

    except Exception as error:

        if connection is not None:
            connection.rollback()

        print("Error adding donation:", error)

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()