
from database import get_connection


def view_events():
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

        print("\n========== AVAILABLE NGO EVENTS ==========")

        if not events:
            print("No events found.")
        else:
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


def register_for_event(volunteer_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Show available events
        cursor.execute("""
            SELECT event_id, event_name, event_date,
                   location, capacity, status
            FROM events
            WHERE status = 'Active'
            ORDER BY event_date
        """)

        events = cursor.fetchall()

        print("\n========== REGISTER FOR EVENT ==========")

        if not events:
            print("No active events available.")
            return

        for event in events:
            print("\nEvent ID:", event[0])
            print("Event Name:", event[1])
            print("Date:", event[2])
            print("Location:", event[3])
            print("Capacity:", event[4])
            print("Status:", event[5])

        event_id = input(
            "\nEnter the Event ID you want to join: "
        ).strip()

        if not event_id.isdigit():
            print("Please enter a valid Event ID.")
            return

        event_id = int(event_id)

        # Check whether the event exists and is active
        cursor.execute("""
            SELECT event_id, capacity
            FROM events
            WHERE event_id = %s AND status = 'Active'
        """, (event_id,))

        event = cursor.fetchone()

        if event is None:
            print("Invalid event ID or event is not active.")
            return

        # Prevent duplicate registration
        cursor.execute("""
            SELECT registration_id
            FROM event_registrations
            WHERE volunteer_id = %s AND event_id = %s
        """, (volunteer_id, event_id))

        if cursor.fetchone():
            print("You are already registered for this event.")
            return

        # Check current registration count
        cursor.execute("""
            SELECT COUNT(*)
            FROM event_registrations
            WHERE event_id = %s
              AND status = 'Registered'
        """, (event_id,))

        registered_count = cursor.fetchone()[0]
        capacity = event[1]

        if capacity is not None and registered_count >= capacity:
            print("Sorry, this event is full.")
            return

        # Save registration
        cursor.execute("""
            INSERT INTO event_registrations
                (volunteer_id, event_id, registration_date, status)
            VALUES (%s, %s, CURDATE(), 'Registered')
        """, (volunteer_id, event_id))

        connection.commit()

        print("\nEvent registration successful!")
        print("Event ID:", event_id)

    except Exception as error:
        if connection is not None:
            connection.rollback()

        print("Registration error:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

def view_my_registered_events(volunteer_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT e.event_id,
                   e.event_name,
                   e.event_date,
                   e.location,
                   er.registration_date,
                   er.status
            FROM event_registrations er
            JOIN events e
                ON er.event_id = e.event_id
            WHERE er.volunteer_id = %s
            ORDER BY er.registration_date DESC
        """

        cursor.execute(query, (volunteer_id,))
        registrations = cursor.fetchall()

        print("\n========== MY REGISTERED EVENTS ==========")

        if not registrations:
            print("You have not registered for any events yet.")
        else:
            for event in registrations:
                print("\n" + "-" * 40)
                print("Event ID:", event[0])
                print("Event Name:", event[1])
                print("Event Date:", event[2])
                print("Location:", event[3])
                print("Registration Date:", event[4])
                print("Registration Status:", event[5])

    except Exception as error:
        print("Error fetching registered events:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


