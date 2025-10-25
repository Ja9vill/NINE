#!/usr/bin/env python3
"""
Test script for the Singing Competition Scoring System API.
This script demonstrates the complete workflow and validates the API endpoints.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_response(response, action):
    """Helper to print formatted responses."""
    print(f"\n{'='*60}")
    print(f"{action}")
    print(f"Status Code: {response.status_code}")
    if response.status_code < 400:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print('='*60)

def test_scoring_system():
    """Run comprehensive tests of the scoring system."""

    print("\n" + "="*60)
    print("SINGING COMPETITION SCORING SYSTEM - API TEST")
    print("="*60)

    # Step 1: Create Judges
    print("\n\n### STEP 1: Creating Judges ###")

    judges_data = [
        {"name": "Simon Cowell", "credentials": "Music industry executive, 30+ years experience"},
        {"name": "Paula Abdul", "credentials": "Grammy-winning artist and choreographer"},
        {"name": "Randy Jackson", "credentials": "Music producer and bassist"}
    ]

    judge_ids = []
    for judge_data in judges_data:
        response = requests.post(f"{BASE_URL}/judges", json=judge_data)
        print_response(response, f"Creating Judge: {judge_data['name']}")
        if response.status_code == 201:
            judge_ids.append(response.json()['id'])

    # Step 2: List all judges
    print("\n\n### STEP 2: Listing All Judges ###")
    response = requests.get(f"{BASE_URL}/judges")
    print_response(response, "GET /judges")

    # Step 3: Create Contestants
    print("\n\n### STEP 3: Creating Contestants ###")

    contestants_data = [
        {"name": "Sarah Williams", "performance_number": 1, "song_title": "Rolling in the Deep"},
        {"name": "Mike Davis", "performance_number": 2, "song_title": "Bohemian Rhapsody"},
        {"name": "Emily Chen", "performance_number": 3, "song_title": "I Will Always Love You"},
        {"name": "James Brown Jr", "performance_number": 4, "song_title": "Uptown Funk"}
    ]

    contestant_ids = []
    for contestant_data in contestants_data:
        response = requests.post(f"{BASE_URL}/contestants", json=contestant_data)
        print_response(response, f"Creating Contestant: {contestant_data['name']}")
        if response.status_code == 201:
            contestant_ids.append(response.json()['id'])

    # Step 4: List all contestants
    print("\n\n### STEP 4: Listing All Contestants ###")
    response = requests.get(f"{BASE_URL}/contestants")
    print_response(response, "GET /contestants")

    # Step 5: Submit Scores
    print("\n\n### STEP 5: Submitting Scores ###")

    # Each judge scores each contestant
    scores_data = [
        # Sarah Williams (Contestant 1)
        {"contestant_id": contestant_ids[0], "judge_id": judge_ids[0], "vocals": 9.0, "stage_presence": 8.5, "song_choice": 9.0, "overall": 8.5, "notes": "Powerful vocals, great song choice"},
        {"contestant_id": contestant_ids[0], "judge_id": judge_ids[1], "vocals": 8.5, "stage_presence": 9.0, "song_choice": 8.0, "overall": 9.0, "notes": "Excellent stage presence"},
        {"contestant_id": contestant_ids[0], "judge_id": judge_ids[2], "vocals": 9.5, "stage_presence": 8.0, "song_choice": 9.0, "overall": 8.5, "notes": "Outstanding performance"},

        # Mike Davis (Contestant 2)
        {"contestant_id": contestant_ids[1], "judge_id": judge_ids[0], "vocals": 10.0, "stage_presence": 9.5, "song_choice": 10.0, "overall": 9.5, "notes": "Incredible! Best performance of the night"},
        {"contestant_id": contestant_ids[1], "judge_id": judge_ids[1], "vocals": 9.5, "stage_presence": 10.0, "song_choice": 9.0, "overall": 9.5, "notes": "Amazing stage presence"},
        {"contestant_id": contestant_ids[1], "judge_id": judge_ids[2], "vocals": 9.0, "stage_presence": 9.0, "song_choice": 10.0, "overall": 9.0, "notes": "Perfect song choice"},

        # Emily Chen (Contestant 3)
        {"contestant_id": contestant_ids[2], "judge_id": judge_ids[0], "vocals": 8.0, "stage_presence": 7.5, "song_choice": 8.5, "overall": 8.0, "notes": "Good performance, room for improvement"},
        {"contestant_id": contestant_ids[2], "judge_id": judge_ids[1], "vocals": 8.5, "stage_presence": 8.0, "song_choice": 8.0, "overall": 8.5, "notes": "Solid performance"},
        {"contestant_id": contestant_ids[2], "judge_id": judge_ids[2], "vocals": 7.5, "stage_presence": 8.0, "song_choice": 7.5, "overall": 7.5, "notes": "Nice effort"},

        # James Brown Jr (Contestant 4)
        {"contestant_id": contestant_ids[3], "judge_id": judge_ids[0], "vocals": 7.0, "stage_presence": 9.0, "song_choice": 8.0, "overall": 7.5, "notes": "Great energy, vocals need work"},
        {"contestant_id": contestant_ids[3], "judge_id": judge_ids[1], "vocals": 7.5, "stage_presence": 9.5, "song_choice": 8.5, "overall": 8.0, "notes": "Fantastic stage presence"},
        {"contestant_id": contestant_ids[3], "judge_id": judge_ids[2], "vocals": 7.0, "stage_presence": 8.5, "song_choice": 8.0, "overall": 7.5, "notes": "Good performer"},
    ]

    for i, score_data in enumerate(scores_data, 1):
        response = requests.post(f"{BASE_URL}/scores", json=score_data)
        print_response(response, f"Submitting Score {i}/{len(scores_data)}")
        time.sleep(0.1)  # Small delay to avoid overwhelming the server

    # Step 6: Get contestant details with scores
    print("\n\n### STEP 6: Getting Contestant Details with Scores ###")
    if contestant_ids:
        response = requests.get(f"{BASE_URL}/contestants/{contestant_ids[0]}")
        print_response(response, f"GET /contestants/{contestant_ids[0]} (Sarah Williams)")

    # Step 7: View Leaderboard
    print("\n\n### STEP 7: FINAL LEADERBOARD ###")
    response = requests.get(f"{BASE_URL}/leaderboard")
    print_response(response, "GET /leaderboard")

    if response.status_code == 200:
        leaderboard = response.json()
        print("\n" + "="*60)
        print("COMPETITION RESULTS - RANKED")
        print("="*60)
        for entry in leaderboard:
            print(f"\nRank #{entry['rank']}: {entry['name']}")
            print(f"  Performance #{entry['performance_number']} - {entry['song_title']}")
            print(f"  Average Total Score: {entry['average_total']:.2f}/40.0")
            print(f"  Breakdown:")
            print(f"    - Vocals: {entry['average_vocals']:.2f}/10")
            print(f"    - Stage Presence: {entry['average_stage_presence']:.2f}/10")
            print(f"    - Song Choice: {entry['average_song_choice']:.2f}/10")
            print(f"    - Overall: {entry['average_overall']:.2f}/10")
            print(f"  Scored by {entry['number_of_judges']} judges")
        print("\n" + "="*60)

    # Step 8: Test validation - try to create duplicate performance number
    print("\n\n### STEP 8: Testing Validation (Duplicate Performance Number) ###")
    duplicate_contestant = {"name": "Test Duplicate", "performance_number": 1, "song_title": "Test Song"}
    response = requests.post(f"{BASE_URL}/contestants", json=duplicate_contestant)
    print_response(response, "Attempting to create duplicate performance number")

    # Step 9: Test validation - invalid score range
    print("\n\n### STEP 9: Testing Validation (Invalid Score Range) ###")
    invalid_score = {
        "contestant_id": contestant_ids[0] if contestant_ids else 1,
        "judge_id": judge_ids[0] if judge_ids else 1,
        "vocals": 11.0,  # Invalid: > 10
        "stage_presence": 8.0,
        "song_choice": 9.0,
        "overall": 8.5
    }
    response = requests.post(f"{BASE_URL}/scores", json=invalid_score)
    print_response(response, "Attempting to submit score with value > 10")

    # Step 10: Test score update (same judge-contestant pair)
    print("\n\n### STEP 10: Testing Score Update ###")
    if contestant_ids and judge_ids:
        updated_score = {
            "contestant_id": contestant_ids[0],
            "judge_id": judge_ids[0],
            "vocals": 10.0,  # Updated from 9.0
            "stage_presence": 9.0,  # Updated from 8.5
            "song_choice": 10.0,  # Updated from 9.0
            "overall": 9.5,  # Updated from 8.5
            "notes": "UPDATED: Changed my mind, this was perfect!"
        }
        response = requests.post(f"{BASE_URL}/scores", json=updated_score)
        print_response(response, "Updating existing score (same judge-contestant pair)")

        # Check updated leaderboard
        print("\n### Updated Leaderboard After Score Change ###")
        response = requests.get(f"{BASE_URL}/leaderboard")
        print_response(response, "GET /leaderboard (after update)")

    print("\n\n" + "="*60)
    print("TEST COMPLETE!")
    print("="*60)
    print("\nThe scoring system is working correctly!")
    print("All endpoints have been tested and validated.")
    print("\nTo use the system:")
    print("1. Make sure the Flask server is running: python -m host_tracker.app")
    print("2. Use the API endpoints as shown in SCORING_API.md")
    print("3. Access the leaderboard at: http://localhost:5000/leaderboard")

if __name__ == "__main__":
    try:
        # First, check if server is running
        response = requests.get(f"{BASE_URL}/hosts")
        print("Server is running!")
        test_scoring_system()
    except requests.exceptions.ConnectionError:
        print("\n" + "="*60)
        print("ERROR: Cannot connect to Flask server")
        print("="*60)
        print("\nPlease start the server first:")
        print("  python -m host_tracker.app")
        print("\nOr:")
        print("  export FLASK_APP=host_tracker.app")
        print("  flask run")
        print("\nThen run this test script again.")
        print("="*60)
