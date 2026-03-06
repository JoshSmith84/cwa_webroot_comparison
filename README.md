# CWA - Webroot Comparison

Very simple script to take outputs from CW Automate and Webroot. And return a combined list with pertinent info.

---

## Features

- Takes output CSV's from Automate and Webroot
- Returns single output CSV with 
Device name, domain, last logged in user, detected AV (if not Webroot), last check-in from either portal 
(or states if not present in other)..
- Only built-in modules needed to run
- Fast / lightweight / simple (if applicable)

---

## Requirements

- Python 3+ 
- OS: Windows / macOS / Linux 

---

## Installation

### "Installation" is a loose term

- Take cwa_webroot.py and constants.py, place in a folder with input csv's names to match.
- I use a company variable, and name all the inputs like '<company>_cwa-computers.csv', '<company>_webroot_inventory.csv', etc. See constants.py for an example. As stated above, very simple for now.
- When exporting from CWA, just leave defaults.