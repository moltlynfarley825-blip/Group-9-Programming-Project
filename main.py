"""Console interface for the Court Case Management System."""
from datetime import datetime
from storage import CourtStore

STATUSES = ("Open", "Adjourned", "Closed")


def prompt(label):
    return input(label).strip()


def pause():
    input("\nPress Enter to continue...")


def register_case(store):
    print("\n--- Register Case ---")
    case_number = prompt("Unique case number: ")
    title = prompt("Case title: ")
    case_type = prompt("Case type: ")
    filing_date = prompt("Filing date (YYYY-MM-DD): ")
    status = prompt("Status [Open/Adjourned/Closed] (default Open): ") or "Open"
    try:
        case = store.add_case(case_number, title, case_type, filing_date, status)
        print(f"Case registered successfully. Case ID: {case['case_number']}")
    except ValueError as exc:
        print(f"Could not register case: {exc}")


def manage_parties(store):
    print("\n--- Manage Parties ---")
    print("1. Add party\n2. List parties")
    choice = prompt("Choose: ")
    if choice == "1":
        try:
            party = store.add_party(
                prompt("Case number: "),
                prompt("Party name: "),
                prompt("Role (e.g., Plaintiff, Defendant, Witness): "),
            )
            print(f"Party added. Party ID: {party['party_id']}")
        except ValueError as exc:
            print(f"Could not add party: {exc}")
    elif choice == "2":
        case_number = prompt("Case number (leave blank for all): ")
        parties = store.list_parties(case_number or None)
        if not parties:
            print("No party records found.")
        for p in parties:
            print(f"{p['party_id']} | {p['case_number']} | {p['name']} | {p['role']}")
    else:
        print("Invalid choice.")


def schedule_hearing(store):
    print("\n--- Schedule Hearing ---")
    try:
        hearing = store.add_hearing(
            prompt("Case number: "),
            prompt("Hearing date (YYYY-MM-DD): "),
            prompt("Hearing time (HH:MM, 24-hour): "),
            prompt("Courtroom: "),
            prompt("Brief fictional note (optional): "),
        )
        print(f"Hearing scheduled. Hearing ID: {hearing['hearing_id']}")
    except ValueError as exc:
        print(f"Could not schedule hearing: {exc}")


def search_case(store):
    print("\n--- Search Case ---")
    term = prompt("Enter case number, title, party name, or status: ")
    results = store.search_cases(term)
    if not results:
        print("No matching cases found.")
    for c in results:
        print(f"{c['case_number']} | {c['title']} | {c['case_type']} | "
              f"Filed: {c['filing_date']} | Status: {c['status']}")


def update_status(store):
    print("\n--- Update Case Status ---")
    try:
        case = store.update_status(
            prompt("Case number: "),
            prompt("New status [Open/Adjourned/Closed]: "),
        )
        print(f"{case['case_number']} status updated to {case['status']}.")
    except ValueError as exc:
        print(f"Could not update status: {exc}")


def view_hearings(store):
    print("\n--- View Hearings by Date ---")
    date = prompt("Hearing date (YYYY-MM-DD): ")
    try:
        hearings = store.hearings_by_date(date)
    except ValueError as exc:
        print(exc)
        return
    if not hearings:
        print("No hearings scheduled for that date.")
    for h in hearings:
        case = store.get_case(h["case_number"])
        title = case["title"] if case else "Unknown case"
        print(f"{h['hearing_time']} | {h['case_number']} | {title} | "
              f"Courtroom: {h['courtroom']} | {h['notes']}")


def basic_reports(store):
    print("\n--- Basic Reports ---")
    open_cases = store.list_cases(status="Open")
    print(f"\nOpen cases: {len(open_cases)}")
    for c in open_cases:
        print(f"- {c['case_number']}: {c['title']}")
    print(f"\nTotal registered cases: {len(store.list_cases())}")
    print(f"Total scheduled hearings: {len(store.list_hearings())}")


def main():
    store = CourtStore()
    actions = {
        "1": register_case,
        "2": manage_parties,
        "3": schedule_hearing,
        "4": search_case,
        "5": update_status,
        "6": view_hearings,
        "7": basic_reports,
    }
    while True:
        print("\n" + "=" * 42)
        print("       COURT CASE MANAGEMENT SYSTEM")
        print("=" * 42)
        print("1. Register Case")
        print("2. Manage Parties")
        print("3. Schedule Hearing")
        print("4. Search Case")
        print("5. Update Case Status")
        print("6. View Hearings by Date")
        print("7. Basic Reports")
        print("8. Exit")
        choice = prompt("\nSelect an option (1-8): ")
        if choice == "8":
            print("Exiting Court Case Management System.")
            break
        action = actions.get(choice)
        if action:
            action(store)
            pause()
        else:
            print("Invalid menu option. Enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
