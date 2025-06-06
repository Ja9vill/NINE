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
