# Singing Competition Scoring System API

A comprehensive scoring system for managing singing competitions with contestants, judges, and scoring.

## Features

- Manage contestants with performance numbers and song selections
- Register judges with credentials
- Submit scores across 4 categories (vocals, stage presence, song choice, overall)
- Real-time leaderboard with rankings
- Automatic score calculation and aggregation
- Validation to prevent duplicate entries

## Scoring Categories

Each contestant is scored by judges on a scale of 0-10 in four categories:

1. **Vocals** - Vocal ability, pitch, tone quality
2. **Stage Presence** - Performance quality, charisma, audience engagement
3. **Song Choice** - Appropriateness and execution of song selection
4. **Overall** - Overall impression and performance

**Total Score**: Sum of all 4 categories (out of 40)
**Average Score**: Total / 4 (out of 10)

## API Endpoints

### Contestants

#### Create a Contestant
```
POST /contestants
Content-Type: application/json

{
  "name": "John Doe",
  "performance_number": 1,
  "song_title": "My Way"
}
```

Response (201 Created):
```json
{
  "id": 1,
  "name": "John Doe",
  "performance_number": 1,
  "song_title": "My Way",
  "created_at": "2025-10-25T12:00:00"
}
```

#### List All Contestants
```
GET /contestants
```

Response:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "performance_number": 1,
    "song_title": "My Way",
    "created_at": "2025-10-25T12:00:00"
  }
]
```

#### Get Contestant Details with Scores
```
GET /contestants/<id>
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "performance_number": 1,
  "song_title": "My Way",
  "created_at": "2025-10-25T12:00:00",
  "scores": [
    {
      "id": 1,
      "judge_name": "Jane Smith",
      "vocals": 9.5,
      "stage_presence": 8.0,
      "song_choice": 9.0,
      "overall": 8.5,
      "total_score": 35.0,
      "average_score": 8.75
    }
  ],
  "average_vocals": 9.5,
  "average_stage_presence": 8.0,
  "average_song_choice": 9.0,
  "average_overall": 8.5,
  "average_total": 35.0
}
```

#### Delete a Contestant
```
DELETE /contestants/<id>
```

### Judges

#### Create a Judge
```
POST /judges
Content-Type: application/json

{
  "name": "Jane Smith",
  "credentials": "Professional vocal coach, 15 years experience"
}
```

Response (201 Created):
```json
{
  "id": 1,
  "name": "Jane Smith",
  "credentials": "Professional vocal coach, 15 years experience",
  "created_at": "2025-10-25T12:00:00"
}
```

#### List All Judges
```
GET /judges
```

#### Get Judge Details with Scores
```
GET /judges/<id>
```

#### Delete a Judge
```
DELETE /judges/<id>
```

### Scores

#### Submit a Score
```
POST /scores
Content-Type: application/json

{
  "contestant_id": 1,
  "judge_id": 1,
  "vocals": 9.5,
  "stage_presence": 8.0,
  "song_choice": 9.0,
  "overall": 8.5,
  "notes": "Excellent performance, great song choice"
}
```

**Notes:**
- All scores must be between 0 and 10
- If a judge submits a score for the same contestant again, it will update the existing score
- Each judge can only have one score per contestant

Response (201 Created):
```json
{
  "id": 1,
  "contestant_id": 1,
  "contestant_name": "John Doe",
  "judge_id": 1,
  "judge_name": "Jane Smith",
  "vocals": 9.5,
  "stage_presence": 8.0,
  "song_choice": 9.0,
  "overall": 8.5,
  "total_score": 35.0,
  "average_score": 8.75,
  "notes": "Excellent performance, great song choice",
  "created_at": "2025-10-25T12:00:00"
}
```

#### List All Scores
```
GET /scores
```

Optional query parameters:
- `contestant_id` - Filter by contestant
- `judge_id` - Filter by judge

Examples:
```
GET /scores?contestant_id=1
GET /scores?judge_id=1
GET /scores?contestant_id=1&judge_id=1
```

#### Get a Specific Score
```
GET /scores/<id>
```

#### Delete a Score
```
DELETE /scores/<id>
```

### Leaderboard

#### Get Competition Leaderboard
```
GET /leaderboard
```

Returns all contestants ranked by their average total score across all judges.

Response:
```json
[
  {
    "rank": 1,
    "contestant_id": 1,
    "name": "John Doe",
    "performance_number": 1,
    "song_title": "My Way",
    "average_vocals": 9.5,
    "average_stage_presence": 8.0,
    "average_song_choice": 9.0,
    "average_overall": 8.5,
    "average_total": 35.0,
    "number_of_judges": 3
  },
  {
    "rank": 2,
    "contestant_id": 2,
    "name": "Mary Johnson",
    "performance_number": 2,
    "song_title": "Respect",
    "average_vocals": 8.0,
    "average_stage_presence": 9.0,
    "average_song_choice": 8.5,
    "average_overall": 8.0,
    "average_total": 33.5,
    "number_of_judges": 3
  }
]
```

## Usage Example

### Complete Workflow

1. **Add Judges**
```bash
curl -X POST http://localhost:5000/judges \
  -H "Content-Type: application/json" \
  -d '{"name": "Simon Cowell", "credentials": "Music industry executive"}'

curl -X POST http://localhost:5000/judges \
  -H "Content-Type: application/json" \
  -d '{"name": "Paula Abdul", "credentials": "Grammy-winning artist"}'
```

2. **Add Contestants**
```bash
curl -X POST http://localhost:5000/contestants \
  -H "Content-Type: application/json" \
  -d '{"name": "Sarah Williams", "performance_number": 1, "song_title": "Rolling in the Deep"}'

curl -X POST http://localhost:5000/contestants \
  -H "Content-Type: application/json" \
  -d '{"name": "Mike Davis", "performance_number": 2, "song_title": "Bohemian Rhapsody"}'
```

3. **Submit Scores**
```bash
# Judge 1 scores Contestant 1
curl -X POST http://localhost:5000/scores \
  -H "Content-Type: application/json" \
  -d '{"contestant_id": 1, "judge_id": 1, "vocals": 9.0, "stage_presence": 8.5, "song_choice": 9.0, "overall": 8.5}'

# Judge 2 scores Contestant 1
curl -X POST http://localhost:5000/scores \
  -H "Content-Type: application/json" \
  -d '{"contestant_id": 1, "judge_id": 2, "vocals": 8.5, "stage_presence": 9.0, "song_choice": 8.0, "overall": 9.0}'
```

4. **View Leaderboard**
```bash
curl http://localhost:5000/leaderboard
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET, PUT, or DELETE
- `201 Created` - Successful POST creating a new resource
- `400 Bad Request` - Invalid input or missing required fields
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate entry (e.g., performance number already exists)

Error responses include a JSON message:
```json
{
  "error": "Description of the error"
}
```

## Database Models

### Contestant
- `id` - Primary key
- `name` - Contestant name
- `performance_number` - Unique performance order number
- `song_title` - Song being performed (optional)
- `created_at` - Timestamp

### Judge
- `id` - Primary key
- `name` - Judge name (unique)
- `credentials` - Professional credentials (optional)
- `created_at` - Timestamp

### Score
- `id` - Primary key
- `contestant_id` - Foreign key to Contestant
- `judge_id` - Foreign key to Judge
- `vocals` - Score 0-10
- `stage_presence` - Score 0-10
- `song_choice` - Score 0-10
- `overall` - Score 0-10
- `notes` - Optional judge notes
- `created_at` - Timestamp
- **Unique constraint**: One score per judge-contestant pair

## Running the Application

```bash
# Install dependencies
pip install flask flask-sqlalchemy apscheduler

# Run the application
python -m host_tracker.app

# Or with flask run
export FLASK_APP=host_tracker.app
flask run
```

The API will be available at `http://localhost:5000`

## Future Enhancements

Potential features for expansion:
- Authentication and authorization for judges
- Multiple competition events/rounds
- Weighted scoring categories
- Score normalization across judges
- Real-time WebSocket updates for leaderboard
- Export results to PDF/Excel
- Audience voting integration
- Historical performance tracking
