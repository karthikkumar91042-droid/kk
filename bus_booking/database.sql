-- ============================================================
--  Bus Booking System  -  MySQL Database Setup
-- ============================================================

CREATE DATABASE IF NOT EXISTS bus_booking_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE bus_booking_db;

-- Users
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100)  NOT NULL,
    email         VARCHAR(150)  NOT NULL UNIQUE,
    phone         VARCHAR(15)   NOT NULL,
    password_hash VARCHAR(256)  NOT NULL,
    is_admin      TINYINT(1)    DEFAULT 0,
    created_at    DATETIME      DEFAULT CURRENT_TIMESTAMP
);

-- Buses
CREATE TABLE IF NOT EXISTS buses (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    bus_number  VARCHAR(20)  NOT NULL UNIQUE,
    bus_name    VARCHAR(100) NOT NULL,
    bus_type    VARCHAR(50)  NOT NULL,
    total_seats INT          NOT NULL,
    amenities   VARCHAR(255)
);

-- Routes
CREATE TABLE IF NOT EXISTS routes (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    source       VARCHAR(100) NOT NULL,
    destination  VARCHAR(100) NOT NULL,
    distance_km  FLOAT        NOT NULL
);

-- Schedules
CREATE TABLE IF NOT EXISTS schedules (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    bus_id           INT    NOT NULL,
    route_id         INT    NOT NULL,
    departure_time   TIME   NOT NULL,
    arrival_time     TIME   NOT NULL,
    travel_date      DATE   NOT NULL,
    price            FLOAT  NOT NULL,
    available_seats  INT    NOT NULL,
    FOREIGN KEY (bus_id)   REFERENCES buses(id)  ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE
);

-- Bookings
CREATE TABLE IF NOT EXISTS bookings (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT          NOT NULL,
    schedule_id    INT          NOT NULL,
    booking_date   DATETIME     DEFAULT CURRENT_TIMESTAMP,
    num_seats      INT          NOT NULL,
    total_amount   FLOAT        NOT NULL,
    status         VARCHAR(20)  DEFAULT 'Confirmed',
    payment_status VARCHAR(20)  DEFAULT 'Paid',
    pnr            VARCHAR(12)  NOT NULL UNIQUE,
    FOREIGN KEY (user_id)     REFERENCES users(id)     ON DELETE CASCADE,
    FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE
);

-- Passengers
CREATE TABLE IF NOT EXISTS passengers (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    booking_id  INT         NOT NULL,
    name        VARCHAR(100) NOT NULL,
    age         INT          NOT NULL,
    gender      VARCHAR(10)  NOT NULL,
    seat_number VARCHAR(5)   NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
);

-- ============================================================
--  Sample seed data
-- ============================================================

-- Sample Buses
INSERT IGNORE INTO buses (bus_number, bus_name, bus_type, total_seats, amenities) VALUES
('KA01AB1234', 'Karnataka Express',  'AC Sleeper',      40, 'WiFi, Charging Port, Blanket, Water Bottle'),
('TN02CD5678', 'Tamil Nadu Travels', 'Non-AC Seater',   45, 'Water Bottle'),
('MH03EF9012', 'Maharashtra Deluxe', 'AC Semi-Sleeper', 36, 'WiFi, Charging Port, Snacks'),
('AP04GH3456', 'Andhra Roadways',    'Sleeper',         40, 'Blanket, Pillow, Charging Port'),
('DL05IJ7890', 'Delhi Super Fast',   'Volvo AC',        45, 'WiFi, USB Charging, Entertainment');

-- Sample Routes
INSERT IGNORE INTO routes (source, destination, distance_km) VALUES
('Bangalore',  'Chennai',    350),
('Chennai',    'Bangalore',  350),
('Mumbai',     'Pune',       150),
('Pune',       'Mumbai',     150),
('Delhi',      'Agra',       200),
('Agra',       'Delhi',      200),
('Hyderabad',  'Bangalore',  570),
('Bangalore',  'Hyderabad',  570),
('Chennai',    'Hyderabad',  630),
('Hyderabad',  'Chennai',    630);

-- Sample Schedules (using today+1 as a reference — adjust dates as needed)
INSERT IGNORE INTO schedules (bus_id, route_id, departure_time, arrival_time, travel_date, price, available_seats) VALUES
(1, 1, '22:00:00', '06:00:00', DATE_ADD(CURDATE(), INTERVAL 1 DAY), 850,  40),
(2, 1, '20:00:00', '04:30:00', DATE_ADD(CURDATE(), INTERVAL 1 DAY), 450,  45),
(3, 3, '07:00:00', '10:30:00', DATE_ADD(CURDATE(), INTERVAL 1 DAY), 350,  36),
(4, 7, '21:00:00', '07:00:00', DATE_ADD(CURDATE(), INTERVAL 1 DAY), 950,  40),
(5, 5, '06:00:00', '09:30:00', DATE_ADD(CURDATE(), INTERVAL 1 DAY), 600,  45),
(1, 2, '08:00:00', '16:00:00', DATE_ADD(CURDATE(), INTERVAL 2 DAY), 850,  40),
(3, 4, '14:00:00', '17:30:00', DATE_ADD(CURDATE(), INTERVAL 2 DAY), 350,  36),
(2, 9, '18:00:00', '08:00:00', DATE_ADD(CURDATE(), INTERVAL 2 DAY), 700,  45);

SELECT 'Database setup complete!' AS Status;
