def compute_risk(features):

    score = 0


    # -------------------
    # Usage decline
    # -------------------

    if features["usage_drop"] < -0.25:
        score += 0.20


    # -------------------
    # Support risk
    # -------------------

    if features["p1"] >= 2:
        score += 0.20

    if features["open"] > 0:
        score += 0.10

    if features["escalated"] > 0:
        score += 0.15


    # -------------------
    # NPS
    # -------------------

    if features["nps"] <= 6:
        score += 0.20

    elif features["nps"] <= 8:
        score += 0.10


    # -------------------
    # CSM Signals
    # -------------------

    if features.get("sentiment")=="negative":
        score += 0.20

    if features.get("churn_intent"):
        score += 0.30


    # -------------------
    # Changelog risk
    # -------------------

    if features.get("sdk_deprecated"):
        score += 0.20

    # NEW
    if features.get("editor_risk"):
        score += 0.15


    # -------------------
    # Signal interaction
    # (VERY IMPORTANT)
    # -------------------

    if (
        features["nps"] <= 6
        and features["open"] > 0
    ):
        score += 0.10


    if (
        features.get("sdk_deprecated")
        and features.get("sentiment")=="negative"
    ):
        score += 0.10


    return min(score,1.0)



def risk_tier(score):

    if score >= .75:
        return "HIGH"

    elif score >= .45:
        return "MEDIUM"

    return "LOW"