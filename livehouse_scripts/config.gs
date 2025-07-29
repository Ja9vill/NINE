// Configuration constants for Livehouse Scheduling system
var SHEETS = {
  FORM_RESPONSES: 'Form Responses',
  ADMIN_REVIEW: 'Admin Review',
  APPROVED_MASTER: 'Approved Events Master',
  CALENDAR: 'Livehouse Calendar View',
  NOTIFICATION: 'Notification Sheet',
  AVAILABLE_SLOTS: 'Available Slots Sheet'
};

var STATUS_COLUMN = 7;     // Column index for Status in Admin Review
var EVENT_TYPE_COLUMN = 3; // Column index for Event Type
var START_COLUMN = 4;      // Column index for Preferred Start Time
var END_COLUMN = 5;        // Column index for Preferred End Time

var SOLO_LIMIT = 2;
var PARTY_LIMIT = 1;
