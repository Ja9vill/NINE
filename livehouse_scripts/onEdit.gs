// Handles status updates within the Admin Review sheet.
// When an entry is marked Approved it is moved to the Approved Events Master.
// Any other status results in the row being moved to the Notification Sheet.
function onEdit(e) {
  var sheet = e.range.getSheet();
  if (sheet.getName() !== SHEETS.ADMIN_REVIEW || e.range.getColumn() !== STATUS_COLUMN) {
    return;
  }

  var status = e.value;
  if (!status) return;
  var row = e.range.getRow();
  var rowData = sheet.getRange(row, 1, 1, sheet.getLastColumn()).getValues()[0];
  var ss = sheet.getParent();

  if (status === 'Approved') {
    ss.getSheetByName(SHEETS.APPROVED_MASTER).appendRow(rowData);
  } else {
    ss.getSheetByName(SHEETS.NOTIFICATION).appendRow(rowData);
  }

  sheet.deleteRow(row);
  UpdateAvailableSlots();
}
