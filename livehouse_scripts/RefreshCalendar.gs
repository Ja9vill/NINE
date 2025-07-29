// Updates the Livehouse Calendar View sheet from the Approved Events Master.
// Intended to be run when an admin clicks a checkbox cell.
function RefreshCalendar() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var calendar = ss.getSheetByName(SHEETS.CALENDAR);
  var master = ss.getSheetByName(SHEETS.APPROVED_MASTER);

  calendar.getDataRange().clearContent().clearFormat();
  var data = master.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var title = row[0];
    var type = row[EVENT_TYPE_COLUMN];
    var start = row[START_COLUMN];
    var end = row[END_COLUMN];
    calendar.appendRow([title, type, start, end]);
    var last = calendar.getLastRow();
    var cell = calendar.getRange(last, 1);
    var color = type === 'Solo' ? '#4285F4' : '#B142F4';
    cell.setFontColor(color);
  }
}
