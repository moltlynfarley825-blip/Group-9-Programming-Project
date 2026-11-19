# Court Case Management System

A beginner-friendly Python console application for fictional case administration.
It is **not** a legal advice system and is not a replacement for official court records.

## Features
- Register cases with unique case numbers, title/type, filing date, and status.
- Add and list parties linked to an existing case.
- Schedule hearings linked to an existing case.
- Search by case number, title, case type, party name, or status.
- Update status (`Open`, `Adjourned`, `Closed`).
- View hearings for a selected date and see basic reports.
- Persist records in CSV files so they remain available after restarting.

## Requirements
- Python 3.9 or newer
- No third-party packages required

## Run
Open a terminal in this folder and run:

```bash
python main.py
```

Choose menu options 1–7 to manage records, or 8 to exit. The first run creates
`data/cases.csv`, `data/parties.csv`, and `data/hearings.csv` automatically.

## Demonstration
1. Select **1. Register Case**.
   - Case number: `CC-2026-001`
   - Case title: `State v. Jordan Sample`
   - Case type: `Criminal`
   - Filing date: `2026-11-19`
   - Status: `Open`
2. Select **2. Manage Parties**, then **1. Add party**.
   - Case number: `CC-2026-001`
   - Party name: `Jordan Sample`
   - Role: `Defendant`
3. Select **3. Schedule Hearing**.
   - Case number: `CC-2026-001`
   - Date: `2026-12-03`
   - Time: `09:30`
   - Courtroom: `Courtroom A`
   - Note: `Initial hearing (fictional)`
4. Select **4. Search Case** and search `Jordan Sample`.
5. Select **5. Update Case Status** and change the case to `Adjourned`.
6. Select **6. View Hearings by Date** and enter `2026-12-03`.
7. Select **7. Basic Reports**.

## Run tests
From this folder:

```bash
python -m unittest discover -s tests -v
```

The tests cover case registration, CSV persistence after restart, duplicate IDs,
case searching, party relationships, hearing validation/scheduling, and status
updates.

## CSV structure
- `cases.csv`: `case_number,title,case_type,filing_date,status`
- `parties.csv`: `party_id,case_number,name,role`
- `hearings.csv`: `hearing_id,case_number,hearing_date,hearing_time,courtroom,notes`

## Validation and limitations
- Dates must be valid `YYYY-MM-DD`; times must be valid 24-hour `HH:MM`.
- A hearing or party cannot be added unless its case already exists.
- Names and case details must be fictional. Keep notes brief and do not enter
  confidential information.
- Automatic courtroom conflict detection and document management are outside
  this project's scope.
