"""CSV-backed storage and business rules for the case management project."""
import csv
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent / "data"
CASE_FIELDS = ["case_number", "title", "case_type", "filing_date", "status"]
PARTY_FIELDS = ["party_id", "case_number", "name", "role"]
HEARING_FIELDS = ["hearing_id", "case_number", "hearing_date", "hearing_time",
                  "courtroom", "notes"]


def validate_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError("Date must be a valid date in YYYY-MM-DD format.")


def validate_time(value):
    try:
        datetime.strptime(value, "%H:%M")
    except (TypeError, ValueError):
        raise ValueError("Time must be valid and use 24-hour HH:MM format.")


class CourtStore:
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.cases_file = self.data_dir / "cases.csv"
        self.parties_file = self.data_dir / "parties.csv"
        self.hearings_file = self.data_dir / "hearings.csv"
        self._ensure_file(self.cases_file, CASE_FIELDS)
        self._ensure_file(self.parties_file, PARTY_FIELDS)
        self._ensure_file(self.hearings_file, HEARING_FIELDS)

    @staticmethod
    def _ensure_file(path, fields):
        if not path.exists():
            with path.open("w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=fields).writeheader()

    @staticmethod
    def _read(path):
        with path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    @staticmethod
    def _write(path, fields, rows):
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def _required(value, label):
        value = (value or "").strip()
        if not value:
            raise ValueError(f"{label} is required.")
        return value

    def list_cases(self, status=None):
        cases = self._read(self.cases_file)
        return [c for c in cases if status is None or c["status"].lower() == status.lower()]

    def get_case(self, case_number):
        key = (case_number or "").strip().lower()
        return next((c for c in self.list_cases() if c["case_number"].lower() == key), None)

    def add_case(self, case_number, title, case_type, filing_date, status="Open"):
        case_number = self._required(case_number, "Case number")
        title = self._required(title, "Case title")
        case_type = self._required(case_type, "Case type")
        validate_date(filing_date)
        status = self._required(status, "Status").title()
        if status not in ("Open", "Adjourned", "Closed"):
            raise ValueError("Status must be Open, Adjourned, or Closed.")
        if self.get_case(case_number):
            raise ValueError("That case number already exists.")
        case = dict(case_number=case_number, title=title, case_type=case_type,
                    filing_date=filing_date, status=status)
        rows = self.list_cases()
        rows.append(case)
        self._write(self.cases_file, CASE_FIELDS, rows)
        return case

    def add_party(self, case_number, name, role):
        case_number = self._required(case_number, "Case number")
        if not self.get_case(case_number):
            raise ValueError("The case number does not exist. Register the case first.")
        name = self._required(name, "Party name")
        role = self._required(role, "Party role")
        rows = self._read(self.parties_file)
        party = {"party_id": str(max([int(x["party_id"]) for x in rows] or [0]) + 1),
                 "case_number": case_number, "name": name, "role": role}
        rows.append(party)
        self._write(self.parties_file, PARTY_FIELDS, rows)
        return party

    def list_parties(self, case_number=None):
        rows = self._read(self.parties_file)
        if case_number:
            rows = [p for p in rows if p["case_number"].lower() == case_number.lower()]
        return rows

    def add_hearing(self, case_number, hearing_date, hearing_time, courtroom, notes=""):
        case_number = self._required(case_number, "Case number")
        if not self.get_case(case_number):
            raise ValueError("The case number does not exist. Register the case first.")
        validate_date(hearing_date)
        validate_time(hearing_time)
        courtroom = self._required(courtroom, "Courtroom")
        rows = self._read(self.hearings_file)
        hearing = {
            "hearing_id": str(max([int(x["hearing_id"]) for x in rows] or [0]) + 1),
            "case_number": case_number, "hearing_date": hearing_date,
            "hearing_time": hearing_time, "courtroom": courtroom,
            "notes": (notes or "").strip()
        }
        rows.append(hearing)
        self._write(self.hearings_file, HEARING_FIELDS, rows)
        return hearing

    def list_hearings(self):
        return self._read(self.hearings_file)

    def hearings_by_date(self, hearing_date):
        validate_date(hearing_date)
        return sorted(
            [h for h in self.list_hearings() if h["hearing_date"] == hearing_date],
            key=lambda h: h["hearing_time"]
        )

    def search_cases(self, term):
        term = (term or "").strip().lower()
        if not term:
            return []
        matching_numbers = {
            p["case_number"].lower() for p in self.list_parties()
            if term in p["name"].lower()
        }
        return [
            c for c in self.list_cases()
            if term in c["case_number"].lower()
            or term in c["title"].lower()
            or term in c["case_type"].lower()
            or term in c["status"].lower()
            or c["case_number"].lower() in matching_numbers
        ]

    def update_status(self, case_number, status):
        case_number = self._required(case_number, "Case number")
        status = self._required(status, "Status").title()
        if status not in ("Open", "Adjourned", "Closed"):
            raise ValueError("Status must be Open, Adjourned, or Closed.")
        rows = self.list_cases()
        for case in rows:
            if case["case_number"].lower() == case_number.lower():
                case["status"] = status
                self._write(self.cases_file, CASE_FIELDS, rows)
                return case
        raise ValueError("Case number not found.")
