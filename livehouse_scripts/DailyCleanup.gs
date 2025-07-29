// Archives past events and removes expired availability each night.
function DailyCleanup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var master = ss.getSheetByName(SHEETS.APPROVED_MASTER);
  var today = new Date();
  var data = master.getDataRange().getValues();
  for (var i = data.length - 1; i >= 1; i--) {
    var end = new Date(data[i][END_COLUMN]);
    if (end < today) {
      master.deleteRow(i + 1);
    }
  }
  UpdateAvailableSlots();
}
