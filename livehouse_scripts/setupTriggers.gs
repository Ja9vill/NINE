// Utility to install all required triggers.
function installTriggers() {
  var ss = SpreadsheetApp.getActive();
  ScriptApp.newTrigger('onFormSubmit')
    .forSpreadsheet(ss)
    .onFormSubmit()
    .create();

  ScriptApp.newTrigger('onEdit')
    .forSpreadsheet(ss)
    .onEdit()
    .create();

  ScriptApp.newTrigger('DailyCleanup')
    .timeBased()
    .everyDays(1)
    .atHour(0)
    .create();
}
