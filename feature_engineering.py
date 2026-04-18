import pandas as pd

def preprocess_accounts(accounts):
    accounts['contract_end_date'] = pd.to_datetime(
    accounts['contract_end_date']
)
    

    today = pd.Timestamp.today()
    accounts['days_to_renewal'] = (
        accounts['contract_end_date'] - today
    ).dt.days

    return accounts


def usage_features(usage):
    usage = usage.sort_values("month")
    trend = usage.groupby("account_id")["api_calls"].pct_change().fillna(0)
    usage["trend"] = trend

    latest = usage.groupby("account_id").tail(1)
    return latest.set_index("account_id")["trend"].to_dict()


def support_features(tickets):
    result = {}
    for acc in tickets['account_id'].unique():
        sub = tickets[tickets['account_id'] == acc]
        result[acc] = {
            "p1": len(sub[sub['priority'] == 'P1']),
            "open": len(sub[sub['status'] == 'Open']),
            "escalated": len(sub[sub['status'] == 'Escalated'])
        }
    return result


def nps_features(nps):
    return nps.set_index("account_id")["score"].to_dict()