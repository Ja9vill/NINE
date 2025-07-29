# Implementation Steps for Livehouse Scheduling Scripts

Follow these steps to deploy the Apps Script modules with the required Google Sheet and Form configuration.

1. **Create the Google Spreadsheet**
   - Open Google Sheets and create a new spreadsheet.
   - Add the following six sheets (tabs) exactly as named:
     1. `Form Responses` – this will be created automatically once the Google Form is linked.
     2. `Admin Review`
     3. `Approved Events Master`
     4. `Livehouse Calendar View`
     5. `Notification Sheet`
     6. `Available Slots Sheet`

2. **Build the Google Form**
   - From the spreadsheet, choose **Tools → Create a new form**.
   - Add fields with the labels and types listed in the implementation package:
     - **Event Title** – Short answer (max 15 characters)
     - **Poppo UID** – Short answer (required)
     - **Event Type** – Dropdown with options `Solo` or `Party`
     - **Preferred Start Time** – Dropdown pulling from `Available Slots Sheet`
     - **Preferred End Time** – Dropdown pulled from the same sheet; ensure the duration is between 30&nbsp;minutes and 2&nbsp;hours
     - **Audition Video Link** – Paragraph or Link field (must be public)
   - Link the form to the spreadsheet so responses populate the `Form Responses` sheet.

3. **Create the Apps Script project**
   - Open **Extensions → Apps Script** from the spreadsheet.
   - Delete any boilerplate code file.
   - For each `.gs` file in this repository's `livehouse_scripts` folder, create a matching script file and paste in the code.
   - Ensure `config.gs` is added first so constants are available to the other modules.

4. **Install Triggers**
   - In the Apps Script editor, run the `installTriggers` function located in `setupTriggers.gs`.
   - Approve the authorization prompts so the script may access the spreadsheet and manage triggers.

5. **Verify Sheet Structure**
   - Confirm that the sheet names in `config.gs` match the names of your tabs.
   - If you use different names, update the constants accordingly before running the scripts.

6. **Test the Workflow**
   - Submit a test entry via the Google Form.
   - Check that the entry appears in the `Admin Review` sheet with status set to `Pending`.
   - Change the status to `Approved` or another value and verify that rows move to the proper sheet and that available slots update.
   - Use the checkbox in `Livehouse Calendar View` to refresh the calendar display.

7. **Daily Automation**
   - The `DailyCleanup` trigger runs automatically at midnight. It archives past events and clears expired availability.
   - You can adjust the time by editing `setupTriggers.gs` before running `installTriggers`.

These steps recreate the entire scheduling workflow from the Livehouse Scheduling Agent Implementation Package.
