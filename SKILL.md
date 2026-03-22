---
name: clawwork-learning-checkin
description: Workplace check-in skill for Agent (小龙虾) with personalized greetings and motivation
metadata: { "copaw": { "emoji": "work" } }
---

# Clawwork Learning Check-in Skill

A workplace check-in skill that wraps the learning-checkin skill with personalized features for Agent (小龙虾).

## Overview

This skill provides:
- Workplace check-in functionality (wraps learning-checkin)
- Personalized greetings with nickname support
- Random daily check-in messages (no repetition)
- Version checking (non-blocking)

## Prerequisites

This skill requires the **learning-checkin** skill to be installed. On first run:
1. The skill will check if learning-checkin is installed
2. If not, it will ask the user if they want to install it
3. If approved, install from: https://clawhub.ai/daizongyu/learning-checkin

## Data Storage

All data is stored locally in a `data` subfolder next to the skill:

```
<skill_directory>/data/
├── profile.json      - User profile (nickname, language)
├── greetings.json    - Greeting history (to avoid repetition)
└── version.txt       - Current skill version
```

## Commands

### 1. Check if learning-checkin is installed

```bash
python <skill_path>/clawwork_checkin.py check-installed
```

**Returns:**
- `installed` - Whether learning-checkin is installed
- `path` - Path where learning-checkin was found
- `needs_installation` - True if needs installation
- `install_url` - URL to install learning-checkin

**Agent action:**
- Run this on first interaction
- If not installed, ask user: "Would you like me to install the learning-checkin skill first?"
- If user agrees, install using appropriate method

### 2. Get Welcome Message

```bash
python <skill_path>/clawwork_checkin.py welcome
```

**Returns:**
- `message` - Random welcome message (work-focused, encouraging)
- `version` - Current skill version

**Agent action:**
- Show welcome message to encourage check-in
- This should be a fresh, energetic message each time

### 3. Perform Check-in

```bash
python <skill_path>/clawwork_checkin.py checkin
```

**Returns:**
- `success` - Whether check-in succeeded
- `streak` - Current streak count
- `message` - Celebration message
- `daily_greeting` - Random greeting to ask user
- `nickname` - User's saved nickname
- `note` - Version check URL

**Agent action:**
1. First ensure learning-checkin is installed
2. Run checkin command
3. Show success message with streak
4. Ask the daily_greeting question naturally

### 4. Get Random Daily Greeting

```bash
python <skill_path>/clawwork_checkin.py greeting
```

**Returns:**
- `greeting` - Random greeting not used recently

**Use:** Can be called after check-in to get a unique greeting.

### 5. Get Version Info

```bash
python <skill_path>/clawwork_checkin.py version
```

**Returns:**
- `version` - Current version
- `check_url` - URL to check for updates
- `note` - Instructions

**Note:** Version checking is non-blocking. The skill mentions the URL but does not perform actual network checks during normal operation.

### 6. Get/Set User Profile

```bash
# Get profile
python <skill_path>/clawwork_checkin.py profile

# Set nickname
python <skill_path>/clawwork_checkin.py set-nickname <name>

# Set language preference
python <skill_path>/clawwork_checkin.py set-language <lang>
```

### 7. Get Status

```bash
python <skill_path>/clawwork_checkin.py status
```

**Returns:**
- `checked_in_today` - Whether user has checked in today
- `streak` - Current streak
- `total_checkins` - Total check-ins
- `nickname` - User's saved nickname

## First-Time Setup Flow

1. **Check if learning-checkin is installed**
   - Run `check-installed` command
   - If not installed, ask user to install

2. **Ask for nickname**
   - "What should I call you? (nickname)"
   - Save with `set-nickname` command

3. **Note the language used**
   - Detect from user's first messages
   - Save with `set-language` command

4. **Welcome and encourage**
   - Run `welcome` command
   - Show the encouraging message

## Daily Check-in Flow

1. User says something like "check in" or "I'm done"
2. Agent runs `checkin` command
3. Agent shows success message with streak
4. Agent asks the daily greeting question naturally

## Greeting System

- 25+ unique daily greetings available
- Greetings are tracked to avoid repetition within the same day
- System tracks last 10 used greetings
- Resets daily for fresh variety

## Version Checking

- Version is embedded in the skill
- After check-in, skill mentions: "You can check for newer versions at https://github.com/daizongyu/clawwork_learning-checkin"
- No automatic network check during normal flow (non-blocking)
- User/Agent can manually check GitHub for updates

## Technical Notes

- All messages are in **English** only (no emoji, UTF-8 encoded)
- Compatible with Windows, Linux, macOS
- Uses Python standard library only (no external dependencies)
- All file paths are relative to the skill directory
- Does not use absolute paths or copaw-specific paths
- Designed to work with OpenClaw, copaw, and other tools
- Subprocess calls to learning-checkin have 10-second timeout

## Customization

Users can customize:
- Their nickname (stored in profile.json)
- Language preference (for future message routing)

## Version

Current version: 1.0.0

Check for updates: https://github.com/daizongyu/clawwork_learning-checkin

## Agent Guidelines

### First Interaction
1. Run `check-installed` to verify learning-checkin
2. If not installed:
   - "I need the learning-checkin skill to work. Would you like me to install it?"
   - If yes, help install
3. Ask for nickname: "What would you like me to call you?"
4. Remember the language they use
5. Run `welcome` and show encouraging message
6. Prompt for first check-in

### Daily Check-in
1. User indicates they want to check in
2. Run `checkin` command
3. Show streak and success message
4. Ask the daily greeting naturally (from response)
5. Converse based on their response

### Language
- Always respond in the language the user established
- If unsure, default to English

### Version
- Do not emphasize version checking
- Simply mention the URL after successful check-in
- Let the Agent/user decide if they want to check manually