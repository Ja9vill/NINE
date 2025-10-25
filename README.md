# NINE

This repository contains a Flask application with two main features:

1. **Host Tracker** - Track and monitor host progress
2. **Singing Competition Scoring System** - Complete scoring system for managing singing competitions

## Features

### Host Tracker
- Track host progress with timestamps
- Background scheduler for automatic profile updates
- Web form interface for progress management

### Singing Competition Scoring System
- Manage contestants with performance numbers
- Register judges with credentials
- Score performances across 4 categories (vocals, stage presence, song choice, overall)
- Real-time leaderboard with rankings
- Comprehensive validation and error handling

## Setup

1. Install Python dependencies:
   ```bash
   pip install Flask Flask-SQLAlchemy APScheduler requests
   ```

2. Run the server:
   ```bash
   python -m host_tracker.app
   ```
   Or using Flask CLI:
   ```bash
   export FLASK_APP=host_tracker.app
   flask run
   ```

The server will start on `http://127.0.0.1:5000`.

## Usage

### Host Tracker

Visit `http://127.0.0.1:5000/progress_form` to update progress for existing
hosts. You can query current host data via `GET /hosts` and update progress via
`POST /hosts/<id>/progress`.

### Singing Competition Scoring System

For detailed API documentation, see [SCORING_API.md](SCORING_API.md).

#### Quick Start

1. **Create Judges:**
   ```bash
   curl -X POST http://localhost:5000/judges \
     -H "Content-Type: application/json" \
     -d '{"name": "Simon Cowell", "credentials": "Music executive"}'
   ```

2. **Create Contestants:**
   ```bash
   curl -X POST http://localhost:5000/contestants \
     -H "Content-Type: application/json" \
     -d '{"name": "Sarah Williams", "performance_number": 1, "song_title": "Rolling in the Deep"}'
   ```

3. **Submit Scores:**
   ```bash
   curl -X POST http://localhost:5000/scores \
     -H "Content-Type: application/json" \
     -d '{"contestant_id": 1, "judge_id": 1, "vocals": 9.0, "stage_presence": 8.5, "song_choice": 9.0, "overall": 8.5}'
   ```

4. **View Leaderboard:**
   ```bash
   curl http://localhost:5000/leaderboard
   ```

#### Testing

Run the comprehensive test script to validate all features:
```bash
# Make sure the server is running first
python test_scoring_api.py
```

## API Endpoints

### Host Tracker
- `GET /hosts` - List all hosts
- `POST /hosts/<id>/progress` - Update host progress
- `GET /progress_form` - Web interface for updates

### Scoring System
- `POST /contestants` - Create contestant
- `GET /contestants` - List contestants
- `GET /contestants/<id>` - Get contestant with scores
- `DELETE /contestants/<id>` - Delete contestant
- `POST /judges` - Create judge
- `GET /judges` - List judges
- `GET /judges/<id>` - Get judge with scores
- `DELETE /judges/<id>` - Delete judge
- `POST /scores` - Submit/update score
- `GET /scores` - List scores (with filtering)
- `GET /scores/<id>` - Get specific score
- `DELETE /scores/<id>` - Delete score
- `GET /leaderboard` - View competition rankings

## Documentation

- [Scoring System API Documentation](SCORING_API.md) - Complete API reference and examples
- [Test Script](test_scoring_api.py) - Automated testing and examples

## Database

The application uses SQLite for data storage:
- `hosts.db` - Contains all data for both host tracking and scoring system

Database models:
- **Host** - Host tracking data
- **Contestant** - Competition contestants
- **Judge** - Competition judges
- **Score** - Performance scores with 4 categories
