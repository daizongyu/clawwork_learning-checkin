#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clawwork Learning Check-in Skill
A workplace check-in skill for Agent (小龙虾) with personalized greetings.
"""

import os
import sys
import json
import datetime
import random

# Fix Windows console encoding for UTF-8
if sys.platform == "win32":
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# Configuration
VERSION = "1.0.0"
VERSION_CHECK_URL = "https://github.com/daizongyu/clawwork_learning-checkin"

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Data will be stored in a 'data' subfolder next to the script
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
PROFILE_FILE = os.path.join(DATA_DIR, "profile.json")
GREETINGS_FILE = os.path.join(DATA_DIR, "greetings.json")
VERSION_FILE = os.path.join(DATA_DIR, "version.txt")

# Default messages in English only (no emoji)
WELCOME_MESSAGES = [
    "Welcome to work! Time to check in and start your productive day!",
    "Good morning! Ready to check in and make today count?",
    "It's work time! Let's check in and get energized!",
    "New day, new opportunities! Time to check in!",
    "Work mode activated! Check in and let's do this!",
    "Another day to be productive! Check in now!",
    "Let's make today amazing! Start with a check-in!",
    "Ready to tackle the day? Check in first!",
    "Work awaits! Check in and get ready to shine!",
    "Fresh start today! Check in and let's go!"
]

# Post check-in greetings (randomized, no repetition)
DAILY_GREETINGS = [
    "How are you feeling today?",
    "What's your plan for today?",
    "Ready to make today productive?",
    "How's your energy level this morning?",
    "Any exciting tasks on your plate today?",
    "What's the most important thing you want to accomplish today?",
    "How's everything going so far?",
    "What are you looking forward to today?",
    "Any challenges you're ready to tackle?",
    "How can I help make your day better?",
    "What's top of your mind today?",
    "Ready to make progress on your goals?",
    "How's the morning treating you?",
    "Any fun plans after work?",
    "What did you sleep well?",
    "Coffee or tea today?",
    "How's the weather treating you?",
    "Any meetings you're excited about?",
    "What's one thing you want to learn today?",
    "How's your week going so far?",
    "Any wins you're celebrating today?",
    "What's keeping you busy these days?",
    "How do you feel about today's schedule?",
    "Any deadlines coming up?",
    "What motivates you most today?"
]


def ensure_dir():
    """Ensure data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_profile():
    """Load user profile (nickname, language, etc.)."""
    if not os.path.exists(PROFILE_FILE):
        return {
            "nickname": None,
            "language": None,
            "first_run": True,
            "initialized_at": None
        }
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "nickname": None,
            "language": None,
            "first_run": True,
            "initialized_at": None
        }


def save_profile(profile):
    """Save user profile."""
    ensure_dir()
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def load_greetings():
    """Load greeting history to avoid repetition."""
    if not os.path.exists(GREETINGS_FILE):
        return {
            "used_greetings": [],
            "last_checkin_date": None
        }
    try:
        with open(GREETINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "used_greetings": [],
            "last_checkin_date": None
        }


def save_greetings(greetings):
    """Save greeting history."""
    ensure_dir()
    with open(GREETINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(greetings, f, ensure_ascii=False, indent=2)


def get_today():
    """Get today's date string."""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_random_greeting():
    """Get a random greeting that hasn't been used recently."""
    greetings_data = load_greetings()
    used_today = greetings_data.get("used_greetings", [])
    last_date = greetings_data.get("last_checkin_date", "")

    # Reset used greetings if it's a new day
    today = get_today()
    if last_date != today:
        used_today = []

    # Filter out recently used greetings
    available_greetings = [g for g in DAILY_GREETINGS if g not in used_today]

    # If all greetings used, reset and allow all
    if not available_greetings:
        available_greetings = DAILY_GREETINGS.copy()

    # Pick a random greeting
    greeting = random.choice(available_greetings)

    # Update greeting history
    used_today.append(greeting)
    greetings_data["used_greetings"] = used_today[-10:]  # Keep last 10
    greetings_data["last_checkin_date"] = today
    save_greetings(greetings_data)

    return greeting


def get_version():
    """Return current version."""
    return VERSION


def check_learning_checkin_installed():
    """Check if learning-checkin skill is installed."""
    # Check common locations
    possible_paths = []

    # Current directory (skill next to this one)
    possible_paths.append(os.path.join(SCRIPT_DIR, "..", "learning-checkin"))
    possible_paths.append(os.path.join(SCRIPT_DIR, "..", "learning_checkin"))

    # Parent of parent
    possible_paths.append(os.path.join(SCRIPT_DIR, "..", "..", "learning-checkin"))

    # Look in active_skills
    if "COPAW_DIR" in os.environ:
        possible_paths.append(os.path.join(os.environ["COPAW_DIR"], "active_skills", "learning-checkin"))

    # Check if learning_checkin.py exists in any of these paths
    for path in possible_paths:
        check_file = os.path.join(path, "learning_checkin.py")
        if os.path.exists(check_file):
            return True, path

    return False, None


def get_welcome_message():
    """Get a random welcome message."""
    return random.choice(WELCOME_MESSAGES)


def get_checkin_success_message(streak):
    """Get check-in success message."""
    if streak == 1:
        return "Check-in successful! Great start to your work day!"
    elif streak == 7:
        return "One week streak! Keep up the excellent work!"
    elif streak == 30:
        return "30 days! You're building an amazing habit!"
    elif streak == 100:
        return "100 days! You are a true professional!"
    else:
        messages = [
            f"Checked in! {streak} days and counting!",
            f"Success! {streak} consecutive days!",
            f"Done! {streak} day streak - keep it going!",
            f"Check-in complete! {streak} days strong!"
        ]
        return random.choice(messages).format(streak=streak)


# CLI Interface
def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("Usage: python clawwork_checkin.py <command> [args]")
        print("Commands:")
        print("  check-installed    - Check if learning-checkin is installed")
        print("  welcome            - Get welcome message")
        print("  greeting           - Get random daily greeting")
        print("  checkin            - Perform workplace check-in")
        print("  version            - Get current version")
        print("  profile            - Get user profile")
        print("  set-nickname <name> - Set user nickname")
        print("  set-language <lang> - Set user language")
        print("  status             - Get check-in status")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "check-installed":
        installed, path = check_learning_checkin_installed()
        result = {
            "installed": installed,
            "path": path,
            "needs_installation": not installed,
            "install_url": "https://clawhub.ai/daizongyu/learning-checkin"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "welcome":
        result = {
            "message": get_welcome_message(),
            "version": VERSION
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "greeting":
        result = {
            "greeting": get_random_greeting()
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "checkin":
        # First check if learning-checkin is installed
        installed, path = check_learning_checkin_installed()
        if not installed:
            result = {
                "success": False,
                "error": "learning-checkin not installed",
                "needs_installation": True,
                "install_url": "https://clawhub.ai/daizongyu/learning-checkin",
                "message": "Please install learning-checkin first"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)

        # Call learning-checkin's checkin command
        checkin_script = os.path.join(path, "learning_checkin.py")
        import subprocess

        try:
            proc = subprocess.run(
                [sys.executable, checkin_script, "checkin"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="ignore"
            )
            if proc.returncode == 0:
                try:
                    checkin_result = json.loads(proc.stdout)
                    # Get profile for personalized response
                    profile = load_profile()
                    nickname = profile.get("nickname", "friend")

                    # Get check-in streak from learning-checkin
                    streak = checkin_result.get("streak", 0)

                    # Get random greeting for after check-in
                    greeting = get_random_greeting()

                    result = {
                        "success": True,
                        "streak": streak,
                        "message": get_checkin_success_message(streak),
                        "daily_greeting": greeting,
                        "nickname": nickname,
                        "note": f"You can check for newer versions at {VERSION_CHECK_URL}"
                    }
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    result = {
                        "success": True,
                        "message": "Check-in recorded!",
                        "daily_greeting": get_random_greeting()
                    }
                    print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                result = {
                    "success": False,
                    "error": proc.stderr or "Unknown error",
                    "message": "Check-in failed"
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
        except subprocess.TimeoutExpired:
            result = {
                "success": True,
                "message": "Check-in may have succeeded (timeout)",
                "note": "Version check timed out, skipping"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "message": "Check-in failed"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "version":
        result = {
            "version": VERSION,
            "check_url": VERSION_CHECK_URL,
            "note": "Check the URL above for the latest version"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "profile":
        profile = load_profile()
        print(json.dumps(profile, ensure_ascii=False, indent=2))

    elif command == "set-nickname":
        if len(sys.argv) < 3:
            print("Usage: python clawwork_checkin.py set-nickname <name>")
            sys.exit(1)
        nickname = sys.argv[2]
        profile = load_profile()
        profile["nickname"] = nickname
        save_profile(profile)
        result = {
            "success": True,
            "nickname": nickname,
            "message": f"Nickname set to: {nickname}"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "set-language":
        if len(sys.argv) < 3:
            print("Usage: python clawwork_checkin.py set-language <lang>")
            print("Example: python clawwork_checkin.py set-language zh")
            sys.exit(1)
        lang = sys.argv[2]
        profile = load_profile()
        profile["language"] = lang
        save_profile(profile)
        result = {
            "success": True,
            "language": lang,
            "message": f"Language set to: {lang}"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "status":
        # Check learning-checkin status
        installed, path = check_learning_checkin_installed()
        if not installed:
            result = {
                "checked_in_today": False,
                "learning_checkin_installed": False,
                "message": "Please install learning-checkin first"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(0)

        # Get status from learning-checkin
        checkin_script = os.path.join(path, "learning_checkin.py")
        import subprocess

        try:
            proc = subprocess.run(
                [sys.executable, checkin_script, "status"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="ignore"
            )
            if proc.returncode == 0:
                try:
                    status_result = json.loads(proc.stdout)
                    profile = load_profile()

                    result = {
                        "checked_in_today": status_result.get("checked_in_today", False),
                        "streak": status_result.get("streak", 0),
                        "total_checkins": status_result.get("total_checkins", 0),
                        "learning_checkin_installed": True,
                        "nickname": profile.get("nickname")
                    }
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    result = {
                        "checked_in_today": False,
                        "learning_checkin_installed": True,
                        "error": "Failed to parse status"
                    }
                    print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                result = {
                    "checked_in_today": False,
                    "learning_checkin_installed": True,
                    "error": "Failed to get status"
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
        except subprocess.TimeoutExpired:
            result = {
                "checked_in_today": False,
                "learning_checkin_installed": True,
                "note": "Status check timed out"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            result = {
                "checked_in_today": False,
                "learning_checkin_installed": True,
                "error": str(e)
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()