from bmdm import BioMedDataManager
import argparse
import json

# main function
def main():
    parser = argparse.ArgumentParser(
        description="BioMedDataManager - Manage biomedical data files with metadata"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # boot
    subparsers.add_parser("boot", help="Initialize BMDM in the current directory")

    # config
    config = subparsers.add_parser("config", help="Set user configuration")
    config.add_argument("--user.name", dest="user_name", help="User's full name")
    config.add_argument("--user.email", dest="user_email", help="User's email address")

    # admit
    admit = subparsers.add_parser("admit", help="Add file or directory to BMDM")
    admit.add_argument("path", help="Path to a file or directory")

    # stats
    subparsers.add_parser("stats", help="Show general statistics")

    # tag
    tag = subparsers.add_parser("tag", help="Add or remove tags from an entry")
    tag.add_argument("entry", help="Entry ID or filename")
    tag.add_argument("--add-tag", help="Add tag in format key=value")
    tag.add_argument("--remove-tag", help="Remove tag by key")

    # find
    find = subparsers.add_parser("find", help="Search for matching entries")
    find.add_argument("--patient-id", help="Filter by patient ID")
    find.add_argument("--modality", help="Filter by modality")
    find.add_argument("--study-date", help="Study date or range (YYYYMMDD or YYYYMMDD-YYYYMMDD)")
    find.add_argument("--tag", help="Filter by tag (key=value)")

    # hist
    hist = subparsers.add_parser("hist", help="View history")
    hist.add_argument("--limit", type=int, help="Limit the number of entries")

    # export
    export = subparsers.add_parser("export", help="Export an entry")
    export.add_argument("entry_id", help="ID of the entry to export")
    export.add_argument("target_directory", help="Target directory for exported data")

    # remove
    remove = subparsers.add_parser("remove", help="Remove an entry")
    remove.add_argument("entry_id", help="ID of the entry to remove")

    args = parser.parse_args()
    manager = BioMedDataManager()

    try:
        command = args.command
        result = None
        if command == "boot":
            method = command
            result = manager.boot()
        elif command == "config":
            method = command
            result = manager.config(name=args.user_name, email=args.user_email)
        elif command == "admit":
            method = command
            result = manager.admit(args.path)
        elif command == "stats":
            method = command
            result = manager.stats()
        elif command == "tag":
            method = command
            if args.add_tag:
                key_value = args.add_tag.split('=', 1)
                key = key_value[0]
                value = key_value[1]
                remove_tag = False
            elif args.remove_tag:
                remove_tag = True
                key = args.remove_tag
                value = None

            result = manager.tag(
                id_filename=args.entry,
                key=key,
                value=value,
                remove=remove_tag
            )
        elif command == "find":
            method = command
            study_date = args.study_date
            if study_date and "-" in study_date:
                start, end = study_date.split("-")
                study_date = (start.strip(), end.strip())
            result = manager.find(
                patient_id=args.patient_id,
                modality=args.modality,
                study_date=study_date,
                tag=args.tag
            )
        elif command == "hist":
            method = command
            if args.limit:
                result = manager.hist(args.limit)
            else:
                result = manager.hist(5)
        elif command == "export":
            method = command
            result = manager.export(args.entry_id, args.target_directory)
        elif command == "remove":
            method = command
            result = manager.remove(args.entry_id)
        if result is not None:
            print(json.dumps(result, indent=2))

    except Exception as e:
        manager._log_activity(method, "ERROR", e)
        print(f"[ERROR] {e}")

main()