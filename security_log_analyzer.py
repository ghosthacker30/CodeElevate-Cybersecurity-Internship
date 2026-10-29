
from collections import Counter
from pathlib import Path
import re

# Find the sample log file in this project's folder.
LOG_FILE = Path(__file__).parent / "sample_logs.txt"

# Flag IP addresses with at least five failed attempts.
THRESHOLD = 5


def analyze_logs():
    # Check whether the input file exists.
    if not LOG_FILE.exists():
        print(f"Error: {LOG_FILE.name} was not found.")
        print("Make sure the sample log file is in the same folder.")
        return

    # Counter stores the number of failures for each IP.
    failed_counts = Counter()
    total_events = 0

    # Open the log file and read it one line at a time.
    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            # Skip empty lines.
            if not line:
                continue

            total_events += 1

            # Ignore successful logins.
            if "LOGIN_FAILED" not in line:
                continue

            # Extract the IP address from the IP= field.
            match = re.search(
                r"\bIP=(\d{1,3}(?:\.\d{1,3}){3})\b",
                line
            )

            if match:
                ip_address = match.group(1)
                failed_counts[ip_address] += 1
            else:
                print(
                    f"Warning: No IP found on line {line_number}"
                )

    # Select IP addresses that meet the threshold.
    flagged_ips = {
        ip: count
        for ip, count in failed_counts.items()
        if count >= THRESHOLD
    }

    # Display the security report.
    print("\n========== SECURITY LOG REPORT ==========")
    print(f"Log file: {LOG_FILE.name}")
    print(f"Total non-empty events: {total_events}")

    print("\nFailed login attempts by IP:")

    if failed_counts:
        for ip, count in sorted(failed_counts.items()):
            print(f"  {ip}: {count} failed attempt(s)")
    else:
        print("  No failed login attempts found.")

    print(f"\nFlagged IP addresses ({THRESHOLD}+ failures):")

    if flagged_ips:
        for ip, count in sorted(flagged_ips.items()):
            print(f"  ALERT: {ip} — {count} failed attempts")
    else:
        print("  No IP addresses reached the threshold.")

    print("\nRepeated failures may require investigation.")
    print("They do not prove malicious activity.")
    print("=========================================")


if __name__ == "__main__":
    analyze_logs()
