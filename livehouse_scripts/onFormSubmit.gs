// Triggered when the Google Form is submitted.
// Copies the most recent response to the Admin Review sheet and
// appends a Status column set to "Pending".
function onFormSubmit(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var formSheet = ss.getSheetByName(SHEETS.FORM_RESPONSES);
  var reviewSheet = ss.getSheetByName(SHEETS.ADMIN_REVIEW);
  var lastRow = formSheet.getLastRow();
  var values = formSheet.getRange(lastRow, 1, 1, formSheet.getLastColumn()).getValues()[0];
  // Append row with Pending status
  reviewSheet.appendRow(values.concat(['Pending']));
}
