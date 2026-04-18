import pandas as pd

def load_data():
    accounts = pd.read_csv("data/accounts.csv")
    usage = pd.read_csv("data/usage_metrics.csv")
    tickets = pd.read_csv("data/support_tickets.csv")
    nps = pd.read_csv("data/nps_responses.csv")

    with open("data/csm_notes.txt", "r", encoding="utf-8") as f:
        csm_notes = f.read()

    with open("data/changelog.md", "r", encoding="utf-8") as f:
        changelog = f.read()

    return accounts, usage, tickets, nps, csm_notes, changelog