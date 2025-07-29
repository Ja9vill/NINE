// Rebuilds the Available Slots sheet based on currently approved events.
function UpdateAvailableSlots() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var master = ss.getSheetByName(SHEETS.APPROVED_MASTER);
  var slotSheet = ss.getSheetByName(SHEETS.AVAILABLE_SLOTS);
  slotSheet.clearContents();

  var today = new Date();
  // Generate slots for today + 6 days ahead
  for (var day = 0; day < 7; day++) {
    var date = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 6 + day);
    ['Morning', 'Afternoon', 'Evening'].forEach(function(block) {
      var soloCount = countApproved(master, date, block, 'Solo');
      var partyCount = countApproved(master, date, block, 'Party');
      var soloAvailable = soloCount < SOLO_LIMIT;
      var partyAvailable = partyCount < PARTY_LIMIT;
      if (soloAvailable || partyAvailable) {
        slotSheet.appendRow([date, block, soloAvailable, partyAvailable]);
      }
    });
  }
}

function countApproved(sheet, date, block, type) {
  var data = sheet.getDataRange().getValues();
  var count = 0;
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var rowDate = new Date(row[START_COLUMN]);
    var rowBlock = row[START_COLUMN + 1]; // assume block stored next column
    var rowType = row[EVENT_TYPE_COLUMN];
    if (rowType === type && sameDay(rowDate, date) && rowBlock === block) {
      count++;
    }
  }
  return count;
}

