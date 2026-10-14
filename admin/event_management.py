

from datetime import date
from database import get_connection


def event_management():
    while True:
        print("\n========================================")
        print("          EVENT MANAGEMENT")
        print("========================================")
        print("1. View All Events")
        print("2. Add New Event")
        print("3. Update Event")
        print("4. Delete Event")
        print("5. Back to Admin Dashboard")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_all_events()

        elif choice == "2":
            add_event()

        elif choice == "3":
            update_event()

        elif choice == "4":
            delete_event()

        elif choice == "5":
            print("Returning to Admin Dashboard...")
            break

        else:
            print("Invalid choice! Please try again.")


def view_all_events():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT event_id, event_name, description,
                   event_date, location, capacity, status
            FROM events
            ORDER BY event_date
        """

        cursor.execute(query)
        events = cursor.fetchall()

        print("\n========== ALL EVENTS ==========")

        if not events:
            print("No events found.")
            return

        for event in events:
            print("\n" + "-" * 40)
            print("Event ID:", event[0])
            print("Event Name:", event[1])
            print("Description:", event[2])
            print("Event Date:", event[3])
            print("Location:", event[4])
            print("Capacity:", event[5])
            print("Status:", event[6])

    except Exception as error:
        print("Error fetching events:", error)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def add_event():
    connection = None
    cursor = None

    try:
        event_name = input("Enter event name: ").strip()
        description = input("Enter event description: ").strip()
        event_date_input = input("Enter event date (YYYY-MM-DD): ").strip()
        location = input("Enter event location: ").strip()
        capacity_input = input("Enter event capacity: ").strip()

        if not event_name or not event_date_input or not location:
            print("Event name, date and location are required.")
            return

        event_date = date.fromisoformat(event_date_input)
        capacity = int(capacity_input)

        if capacity <= 0:
            print("Capacity must be greater than zero.")
            return

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO events
                (event_name, description, event_date,
                 location, capacity, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            event_name,
            description,
            event_date,
            location,
            capacity,
            "Active"
        )

        cursor.execute(query, values)
        connection.commit()

        print("\nEvent added successfully!")
        print("New Event ID:", cursor.lastrowid)

    except ValueError:
        print("Invalid input! Use YYYY-MM-DD date and a numeric capacity.")

    except Exception as error:
        if connection is not None:
            connection.rollback()
        print("Error adding event:", error)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def update_event():
    connection = None
    cursor = None

    try:
        event_id = int(input("Enter Event ID to update: "))

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT event_id, event_name, description, event_date,
                   location, capacity, status
            FROM events
            WHERE event_id = %s
            """,
            (event_id,)
        )

        event = cursor.fetchone()

        if not event:
            print("Event not found!")
            return

        print("\n========== CURRENT EVENT DETAILS ==========")
        print("Event Name:", event[1])
        print("Description:", event[2])
        print("Event Date:", event[3])
        print("Location:", event[4])
        print("Capacity:", event[5])
        print("Status:", event[6])

        print("\nPress Enter to keep the current value.")

        event_name = input("New event name: ").strip() or event[1]
        description = input("New description: ").strip() or event[2]

        date_input = input("New event date (YYYY-MM-DD): ").strip()
        location = input("New location: ").strip() or event[4]
        capacity_input = input("New capacity: ").strip()
        status_input = input("New status (Active/Inactive): ").strip()

        event_date = event[3]
        if date_input:
            event_date = date.fromisoformat(date_input)

        capacity = event[5]
        if capacity_input:
            capacity = int(capacity_input)

        status = status_input or event[6]

        if capacity <= 0:
            print("Capacity must be greater than zero.")
            return

        if status not in ("Active", "Inactive"):
            print("Status must be Active or Inactive.")
            return

        cursor.execute(
            """
            UPDATE events
            SET event_name = %s,
                description = %s,
                event_date = %s,
                location = %s,
                capacity = %s,
                status = %s
            WHERE event_id = %s
            """,
            (
                event_name,
                description,
                event_date,
                location,
                capacity,
                status,
                event_id
            )
        )

        connection.commit()

        if cursor.rowcount > 0:
            print("\nEvent updated successfully!")
        else:
            print("\nNo changes were made.")

    except ValueError:
        print("Invalid input! Check Event ID, date and capacity.")

    except Exception as error:
        if connection is not None:
            connection.rollback()
        print("Error updating event:", error)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def delete_event():
    connection = None
    cursor = None

    try:
        event_id = int(input("Enter Event ID to delete: "))

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT event_id, event_name FROM events WHERE event_id = %s",
            (event_id,)
        )

        event = cursor.fetchone()

        if not event:
            print("Event not found!")
            return

        print("\nEvent ID:", event[0])
        print("Event Name:", event[1])

        confirm = input(
            "Are you sure you want to delete this event? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Delete cancelled.")
            return

        # Prevent deletion when registrations refer to this event.
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM event_registrations
            WHERE event_id = %s
            """,
            (event_id,)
        )

        registration_count = cursor.fetchone()[0]

        if registration_count > 0:
            print(
                "This event has registrations and cannot be deleted safely."
            )
            print("Consider updating its status to Inactive instead.")
            return

        cursor.execute(
            "DELETE FROM events WHERE event_id = %s",
            (event_id,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            print("\nEvent deleted successfully!")
        else:
            print("\nEvent was not deleted.")

    except ValueError:
        print("Please enter a valid numeric Event ID.")

    except Exception as error:
        if connection is not None:
            connection.rollback()
        print("Error deleting event:", error)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
