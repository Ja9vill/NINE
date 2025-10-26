# NINE

A modern Flask-based Host Tracker application with a sleek black and gold UI theme.
Track and monitor progress metrics for multiple hosts with real-time updates and
automated profile refreshing.

## Features

### Visual & Theme
- **Modern Dashboard UI**: Luxurious black and gold theme with smooth animations and transitions
- **Dark/Light Theme Toggle**: Switch between dark and light modes with persistent preference
- **Responsive Design**: Fully responsive layout that works seamlessly on desktop, tablet, and mobile devices
- **Animated Effects**: Smooth hover effects, progress bar shine animations, and interactive transitions

### Data Management
- **Add Hosts**: Create new hosts with custom names and initial progress through an elegant modal
- **Delete Hosts**: Remove hosts with confirmation dialog to prevent accidental deletion
- **Update Progress**: Real-time progress updates with visual feedback and success notifications
- **Automated Updates**: Background scheduler refreshes host profiles every minute

### Search & Organization
- **Advanced Search**: Real-time search functionality to filter hosts by name
- **Multiple Sort Options**: Sort hosts by name, progress, or ID in ascending/descending order
- **Pagination**: Smart pagination system displaying 6 hosts per page with intuitive navigation
- **Empty State Handling**: Helpful messages when no hosts exist or search returns no results

### Visualization & Analytics
- **Statistics Dashboard**: Real-time overview showing total hosts, average progress, and completed hosts
- **Progress Charts**: Beautiful bar chart visualization showing progress distribution across all hosts
- **Visual Progress Bars**: Animated progress indicators with gold gradient and shine effects
- **Live Status Monitoring**: Active monitoring indicator showing system status

### Data Export
- **CSV Export**: Download all host data as CSV for use in spreadsheets
- **JSON Export**: Export data in JSON format for integration with other systems
- **One-Click Export**: Simple export buttons in the header for quick data extraction

### API & Integration
- **RESTful API**: Full API support for programmatic access
- **CRUD Operations**: Complete Create, Read, Update, Delete operations for hosts
- **JSON Responses**: Standardized JSON responses for easy integration

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

#### Host Management
- `GET /hosts` - Retrieve all hosts with their current progress and metadata
- `POST /hosts` - Create a new host
  ```json
  {
    "name": "Server-01",
    "progress": 0
  }
  ```
- `DELETE /hosts/<id>` - Delete a specific host

#### Progress Updates
- `POST /hosts/<id>/progress` - Update progress for a specific host
  ```json
  {
    "progress": 75
  }
  ```

#### Data Export
- `GET /export/csv` - Download all hosts data as CSV file
- `GET /export/json` - Download all hosts data as JSON file

## Dashboard Features

### Interactive Controls
- **Theme Toggle**: Moon/sun icon in header to switch between dark and light themes
- **Search Bar**: Real-time filtering of hosts by name
- **Sort Dropdown**: Multiple sorting options (name, progress, ID) in both directions
- **Pagination Controls**: Navigate through hosts with previous/next buttons and page numbers
- **Export Buttons**: Quick access to CSV and JSON export in the header

### Host Cards
- **Visual Progress Bars**: Animated gold gradient progress indicators with shine effect
- **Quick Actions**: Update button for instant progress changes
- **Delete Button**: Trash icon to remove hosts (with confirmation)
- **Host Information**: ID badge, name, progress percentage, and last update timestamp
- **Hover Effects**: Cards lift and glow on hover for better interactivity

### Modals
- **Add Host Modal**: Beautiful form to create new hosts with name and initial progress
- **Delete Confirmation**: Safety dialog to prevent accidental deletions
- **Keyboard Support**: Press Escape to close modals, click outside to dismiss
- **Form Validation**: Client-side validation for all input fields

### Statistics & Charts
- **4 Stat Cards**: Total hosts, average progress, completed hosts, live monitoring status
- **Progress Chart**: Canvas-based bar chart showing distribution of progress across hosts
- **Theme-Aware Charts**: Charts automatically adjust colors based on selected theme
- **Hover Animations**: Stat cards animate on hover for enhanced engagement

### User Experience
- **Success Notifications**: Slide-in messages for successful operations
- **Error Handling**: Clear error messages for failed operations
- **Loading States**: Visual feedback during data refresh
- **Responsive Layout**: Adapts to all screen sizes from mobile to desktop
- **Persistent Theme**: Theme preference saved to browser localStorage
- **Smooth Transitions**: All interactions enhanced with CSS transitions and animations
