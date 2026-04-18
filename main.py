import json

from ingestion import load_data

from llm_engine import analyze_csm_notes
from llm_engine import analyze_changelog


# ---------------------------------
# Load everything once
# ---------------------------------

accounts, usage, tickets, nps, csm_notes, changelog = load_data()


# ---------------------------------
# Run LLMs
# ---------------------------------
raw_csm = analyze_csm_notes(csm_notes)

# Remove markdown wrapper
raw_csm = (
    raw_csm
    .replace("```json", "")
    .replace("```", "")
    .strip()
)

csm_output = json.loads(raw_csm)
# csm_output = json.loads(
#     analyze_csm_notes(csm_notes)
# )
raw_change = analyze_changelog(changelog)

raw_change = (
    raw_change
    .replace("```json","")
    .replace("```","")
    .strip()
)

changelog_risk = json.loads(raw_change)
# changelog_risk = json.loads(
#     analyze_changelog(changelog)
# )


# ---------------------------------
# Build features
# ---------------------------------

def build_features(account_id, usage, tickets, nps):

    features = {}

    # ----------------
    # Usage
    # ----------------

    acc_usage = usage[
        usage['account_id']==account_id
    ].sort_values("month")

    if len(acc_usage)>=2:

        last = acc_usage.iloc[-1]['api_calls']

        prev = acc_usage.iloc[-2]['api_calls']

        features["usage_drop"]=(last-prev)/prev

    else:
        features["usage_drop"]=0


    # ----------------
    # Tickets
    # ----------------

    acc_tickets=tickets[
       tickets["account_id"]==account_id
    ]

    features["p1"]=len(
      acc_tickets[
       acc_tickets["priority"]=="P1"
      ]
    )

    features["open"]=len(
      acc_tickets[
       acc_tickets["status"]=="Open"
      ]
    )

    features["escalated"]=len(
      acc_tickets[
       acc_tickets["status"]=="Escalated"
      ]
    )


    # ----------------
    # NPS
    # ----------------

    features["nps"]=nps.get(
       account_id,
       7
    )


    # ----------------
    # CSM signals
    # ----------------

    for item in csm_output:

        if item["account_id"]==account_id:

            features["sentiment"]=item["sentiment"]

            features["churn_intent"]=item["churn_intent"]


    # ----------------
    # Changelog signals
    # ----------------

    features["sdk_deprecated"]=(
      changelog_risk["sdk_deprecated"]
    )

    features["editor_risk"]=(
      changelog_risk["editor_migration_risk"]
    )


    return features