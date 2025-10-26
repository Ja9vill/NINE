# NINE

A modern Flask-based Host Tracker application with a sleek black and gold UI theme.
Track and monitor progress metrics for multiple hosts with real-time updates and
automated profile refreshing.

## Features

- **Modern Dashboard UI**: Elegant black and gold theme with smooth animations
- **Real-time Monitoring**: Live progress tracking with visual progress bars
- **Statistics Overview**: Instant view of total hosts, average progress, and system status
- **RESTful API**: Full API support for programmatic access
- **Automated Updates**: Background scheduler refreshes host profiles every minute
- **Responsive Design**: Works seamlessly on desktop and mobile devices

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

### Web Interface

- **Main Dashboard**: Visit `http://127.0.0.1:5000/` for the modern dashboard UI
- **Legacy Form**: Visit `http://127.0.0.1:5000/progress_form` for the simple form view

### API Endpoints

- `GET /hosts` - Retrieve all hosts with their current progress and metadata
- `POST /hosts/<id>/progress` - Update progress for a specific host
  ```json
  {
    "progress": 75
  }
  ```

## UI Features

- **Host Cards**: Each host displayed in an elegant card with visual progress indicators
- **Live Statistics**: Real-time dashboard showing total hosts and average progress
- **Interactive Updates**: Update host progress directly from the dashboard
- **Smooth Animations**: Professional animations and hover effects
- **Status Indicators**: Visual feedback for updates and system status
