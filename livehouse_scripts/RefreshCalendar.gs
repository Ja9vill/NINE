// Builds a monthly calendar grid in the Livehouse Calendar View sheet and
// colors days that have approved events.
function RefreshCalendar() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var calendar = ss.getSheetByName(SHEETS.CALENDAR);
  var master = ss.getSheetByName(SHEETS.APPROVED_MASTER);

  var month = calendar.getRange(MONTH_CELL).getValue();
  var year = calendar.getRange(YEAR_CELL).getValue();
  if (!month || !year) {
    var today = new Date();
    month = today.getMonth() + 1;
    year = today.getFullYear();
    calendar.getRange(MONTH_CELL).setValue(month);
    calendar.getRange(YEAR_CELL).setValue(year);
  }

  // clear calendar grid
  calendar.getRange(CAL_GRID_START_ROW, CAL_GRID_START_COL,
                    CAL_GRID_ROWS, CAL_GRID_COLS).clearContent().clearFormat();
  var first = new Date(year, month - 1, 1);
  var offset = first.getDay(); // 0=Sun
  var daysInMonth = new Date(year, month, 0).getDate();

  var day = 1;
  for (var r = 0; r < CAL_GRID_ROWS; r++) {
    for (var c = 0; c < CAL_GRID_COLS; c++) {
      var cell = calendar.getRange(CAL_GRID_START_ROW + r,
                                   CAL_GRID_START_COL + c);
      if (r === 0 && c < offset) {
        cell.setValue('');
      } else if (day <= daysInMonth) {
        cell.setValue(day);
        var current = new Date(year, month - 1, day);
        if (hasEvent(master, current)) {
          cell.setBackground('#e8f0fe'); // highlight days with events
        }
        day++;
      } else {
        cell.setValue('');
      }
    }
  }
  displayEventsForDate(new Date(year, month - 1, new Date().getDate()));
}

// returns true if the given date has approved events
function hasEvent(sheet, date) {
  var data = sheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    var start = new Date(data[i][START_COLUMN]);
    if (sameDay(start, date)) return true;
  }
  return false;
}
