# NINE

This repository contains a sample Flask application located in `host_tracker/`.
The application exposes a small API for updating progress on hosts and includes
scheduled tasks that refresh host profile information.

## Setup

1. Install Python dependencies:
   ```bash
   pip install Flask Flask-SQLAlchemy APScheduler
   ```
2. Run the server:
   ```bash
   python host_tracker/app.py
   ```

The server will start on `http://127.0.0.1:5000`. A background scheduler will
update host profiles every minute.

## Usage

Visit `http://127.0.0.1:5000/progress_form` to update progress for existing
hosts. You can query current host data via `GET /hosts` and update progress via
`POST /hosts/<id>/progress`.

## Booking System

A minimal booking application is available in `booking_system/`. It provides simple APIs to manage rooms and create bookings.

### Setup and Run

1. Install dependencies:
   ```bash
   pip install Flask Flask-SQLAlchemy
   ```
2. Start the booking server:
   ```bash
   python booking_system/app.py
   ```

### API

- `POST /rooms` - Create a room. Requires a `name` field.
- `GET /rooms` - List all rooms.
- `POST /bookings` - Create a booking with `room_id`, `user_name`, `start_time`, and `end_time` (ISO 8601 strings).
- `GET /bookings` - List all bookings.
