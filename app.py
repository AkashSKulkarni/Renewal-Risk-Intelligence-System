from flask import Flask, jsonify

from ingestion import load_data
from feature_engineering import preprocess_accounts, nps_features
from main import build_features
from risk_model import compute_risk, risk_tier
from llm_engine import generate_explanation


app = Flask(__name__)


# --------------------------------
# LOAD DATA (ONCE)
# --------------------------------
accounts, usage, tickets, nps, csm, changelog = load_data()

accounts = preprocess_accounts(accounts)
nps_dict = nps_features(nps)


# --------------------------------
# METHODS (BUSINESS LOGIC LAYER)
# --------------------------------

def get_renewal_accounts():
    return accounts[accounts["days_to_renewal"] <= 90]


def get_account_by_id(account_id):
    match = accounts[accounts["account_id"] == account_id]
    return None if match.empty else match.iloc[0]


def calculate_account_risk(account_id, row):

    features = build_features(
        account_id,
        usage,
        tickets,
        nps_dict
    )

    score = compute_risk(features)

    explanation = generate_explanation(features)

    return {
        "account_id": int(account_id),
        "account_name": row["account_name"],
        "risk": risk_tier(score),
        "score": round(score, 2),
        "arr": int(row["arr"]),
        "features": features,
        "explanation": explanation
    }


def get_all_renewal_risks():

    renewals = get_renewal_accounts()

    results = []

    for _, row in renewals.iterrows():
        acc_id = row["account_id"]
        results.append(calculate_account_risk(acc_id, row))

    return results


def get_single_account_risk(account_id):

    row = get_account_by_id(account_id)

    if row is None:
        return None

    return calculate_account_risk(account_id, row)


# --------------------------------
# API LAYER (ENDPOINTS ONLY)
# --------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running"})


@app.route("/renewal-risk", methods=["GET"])
def renewal_risk():

    data = get_all_renewal_risks()

    return jsonify(data)


@app.route("/account/<int:account_id>", methods=["GET"])
def account_risk(account_id):

    result = get_single_account_risk(account_id)

    if result is None:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(result)


# --------------------------------
# MAIN
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)