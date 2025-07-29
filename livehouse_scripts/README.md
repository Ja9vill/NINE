# Livehouse Scheduling Google Apps Script

This directory contains the Apps Script modules for the Poppo platform
Livehouse scheduling workflow. Functions mirror the specification from
the Livehouse Scheduling Agent Implementation Package.

## Modules

- `onFormSubmit.gs` – triggered when hosts submit the request form and
  copies the entry to **Admin Review** with a `Pending` status.
- `onEdit.gs` – listens for status updates in **Admin Review**.
  Approved rows move to **Approved Events Master** while all others are
  sent to the **Notification Sheet**.
- `UpdateAvailableSlots.gs` – recalculates the **Available Slots Sheet**
  based on currently approved events.
- `RefreshCalendar.gs` – populates **Livehouse Calendar View** from the
  approved events, color-coding by event type.
- `DailyCleanup.gs` – archives past events nightly and triggers a slot
  availability refresh.
- `setupTriggers.gs` – utility function to install the required
  triggers.

Constants for sheet names and column positions reside in `config.gs`.
For step-by-step setup instructions, see [IMPLEMENTATION_STEPS.md](IMPLEMENTATION_STEPS.md).
