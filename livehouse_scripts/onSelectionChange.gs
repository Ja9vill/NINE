// Updates the event details pane when a date cell is selected
// in the Livehouse Calendar View sheet.
function onSelectionChange(e) {
  var sheet = e.range.getSheet();
  if (sheet.getName() !== SHEETS.CALENDAR) return;

  var row = e.range.getRow();
  var col = e.range.getColumn();
  if (row < CAL_GRID_START_ROW ||
      row >= CAL_GRID_START_ROW + CAL_GRID_ROWS ||
      col < CAL_GRID_START_COL ||
      col >= CAL_GRID_START_COL + CAL_GRID_COLS) {
    return;
  }

  var day = e.range.getValue();
  if (!day) return;

  var month = sheet.getRange(MONTH_CELL).getValue();
  var year = sheet.getRange(YEAR_CELL).getValue();
  if (!month || !year) return;

  var date = new Date(year, month - 1, day);
  displayEventsForDate(date);
}
