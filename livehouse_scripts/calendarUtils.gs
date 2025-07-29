// Utility functions for the Livehouse calendar view.

// Write events for the specified date into the calendar details pane
function displayEventsForDate(date) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var master = ss.getSheetByName(SHEETS.APPROVED_MASTER);
  var cal = ss.getSheetByName(SHEETS.CALENDAR);
  var start = cal.getRange(DETAIL_START_CELL);
  var rows = 10; // clear 10 rows
  cal.getRange(start.getRow(), start.getColumn(), rows, 4).clearContent();

  var data = master.getDataRange().getValues();
  var out = [];
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var eventDate = new Date(row[START_COLUMN]);
    if (sameDay(eventDate, date)) {
      out.push([row[0], row[EVENT_TYPE_COLUMN], row[START_COLUMN], row[END_COLUMN]]);
    }
  }
  if (out.length > 0) {
    cal.getRange(start.getRow(), start.getColumn(), out.length, 4).setValues(out);
  }
}

// Compare two dates, ignoring time
function sameDay(d1, d2) {
  return d1.getFullYear() === d2.getFullYear() &&
         d1.getMonth() === d2.getMonth() &&
         d1.getDate() === d2.getDate();
}
