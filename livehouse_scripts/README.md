# Livehouse Scheduling Google Apps Script

This directory contains the Apps Script modules for the Poppo platform
Livehouse scheduling workflow. Functions mirror the specification from
the Livehouse Scheduling Agent Implementation Package.

## Modules

- `onFormSubmit.gs` – triggered when hosts submit the request form and copies the entry to **Admin Review** with a `Pending` status.
- `onEdit.gs` – moves rows from **Admin Review** to either **Approved Events Master** or **Notification Sheet** when the status changes.
- `UpdateAvailableSlots.gs` – recalculates the **Available Slots Sheet** based on approved events.
- `RefreshCalendar.gs` – builds the monthly calendar view and highlights days with events.
- `onSelectionChange.gs` – displays a day's events when a calendar cell is selected.
- `calendarUtils.gs` – helper functions shared by calendar scripts.
- `DailyCleanup.gs` – archives past events nightly and refreshes slot availability.
- `setupTriggers.gs` – installs the required triggers.


Constants for sheet names and column positions reside in `config.gs`.
For step-by-step setup instructions, see [IMPLEMENTATION_STEPS.md](IMPLEMENTATION_STEPS.md).
