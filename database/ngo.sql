CREATE DATABASE IF NOT EXISTS ngo_management;

USE ngo_management;


-- 1. Admin Table
CREATE TABLE IF NOT EXISTS admins (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);


-- 2. Volunteer Table
CREATE TABLE IF NOT EXISTS volunteers (
    volunteer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    password VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    skills VARCHAR(200),
    registration_date DATE,
    status VARCHAR(20) DEFAULT 'Active'
);


-- 3. Events Table
CREATE TABLE IF NOT EXISTS events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    event_date DATE,
    location VARCHAR(100),
    capacity INT,
    status VARCHAR(20) DEFAULT 'Active'
);


-- 4. Event Registration Table
CREATE TABLE IF NOT EXISTS event_registrations (
    registration_id INT PRIMARY KEY AUTO_INCREMENT,
    volunteer_id INT,
    event_id INT,
    registration_date DATE,
    status VARCHAR(20) DEFAULT 'Registered',

    FOREIGN KEY (volunteer_id)
    REFERENCES volunteers(volunteer_id),

    FOREIGN KEY (event_id)
    REFERENCES events(event_id)
);


-- 5. Activities Table
CREATE TABLE IF NOT EXISTS activities (
    activity_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT,
    activity_name VARCHAR(100),
    description VARCHAR(255),
    status VARCHAR(20) DEFAULT 'Pending',

    FOREIGN KEY (event_id)
    REFERENCES events(event_id)
);


-- 6. Activity Volunteers Table
CREATE TABLE IF NOT EXISTS activity_volunteers (
    activity_volunteer_id INT PRIMARY KEY AUTO_INCREMENT,
    activity_id INT,
    volunteer_id INT,
    assigned_date DATE,
    status VARCHAR(20) DEFAULT 'Assigned',

    FOREIGN KEY (activity_id)
    REFERENCES activities(activity_id),

    FOREIGN KEY (volunteer_id)
    REFERENCES volunteers(volunteer_id)
);


-- 7. Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT,
    volunteer_id INT,
    attendance_date DATE,
    status VARCHAR(20),

    FOREIGN KEY (event_id)
    REFERENCES events(event_id),

    FOREIGN KEY (volunteer_id)
    REFERENCES volunteers(volunteer_id)
);


-- 8. Donations Table
CREATE TABLE IF NOT EXISTS donations (
    donation_id INT PRIMARY KEY AUTO_INCREMENT,
    donor_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    amount DECIMAL(10,2),
    payment_mode VARCHAR(50),
    donation_date DATE,
    purpose VARCHAR(200)
);


-- 9. Certificates Table
CREATE TABLE IF NOT EXISTS certificates (
    certificate_id INT PRIMARY KEY AUTO_INCREMENT,
    volunteer_id INT,
    event_id INT,
    certificate_number VARCHAR(50) UNIQUE,
    issue_date DATE,
    certificate_path VARCHAR(255),

    FOREIGN KEY (volunteer_id)
    REFERENCES volunteers(volunteer_id),

    FOREIGN KEY (event_id)
    REFERENCES events(event_id)
);


-- Insert default admin
INSERT INTO admins (username, password)
VALUES ('admin', 'admin123');