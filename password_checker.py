
import getpass
import string


def check_password(password):
    # Check five basic password properties.
    checks = {
        "At least 12 characters": len(password) >= 12,
        "Uppercase letter": any(c.isupper() for c in password),
        "Lowercase letter": any(c.islower() for c in password),
        "Digit": any(c.isdigit() for c in password),
        "Special character": any(c in string.punctuation for c in password),
    }

    passed = sum(checks.values())
    suggestions = []

    # Give suggestions for missing requirements.
    if len(password) < 12:
        suggestions.append("Use at least 12 characters.")

    if not checks["Uppercase letter"]:
        suggestions.append("Add an uppercase letter.")

    if not checks["Lowercase letter"]:
        suggestions.append("Add a lowercase letter.")

    if not checks["Digit"]:
        suggestions.append("Add a digit.")

    if not checks["Special character"]:
        suggestions.append("Add a special character.")

    # Simple educational scoring rules.
    if len(password) >= 12 and passed == 5:
        strength = "STRONG"
    elif len(password) >= 8 and passed >= 3:
        strength = "MEDIUM"
    else:
        strength = "WEAK"

    return strength, checks, suggestions


def main():
    print("===== PASSWORD STRENGTH CHECKER =====")
    print("Use a fictional sample password only.")
    print("The password is checked locally and is not saved.")

    # Hide typed characters in the terminal.
    password = getpass.getpass("Enter sample password: ")

    strength, checks, suggestions = check_password(password)

    print("\nPassword checks:")

    for description, passed in checks.items():
        status = "PASS" if passed else "NEEDS IMPROVEMENT"
        print(f"{description}: {status}")

    print(f"\nStrength assessment: {strength}")

    if suggestions:
        print("\nSuggestions:")
        for suggestion in suggestions:
            print(f"- {suggestion}")
    else:
        print("\nAll checks passed.")
        print("Avoid reusing passwords across accounts.")

    print("\n=====================================")


if __name__ == "__main__":
    main()
