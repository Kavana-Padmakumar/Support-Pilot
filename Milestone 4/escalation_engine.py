"""
escalation_engine.py — Milestone 4 Automatic Escalation Rules
Implements strict conditional rules to route tickets needing human intervention.
"""


def check_escalation(ticket_data):
    """
    Evaluate a ticket against all escalation conditions.
    Returns (status, reason) tuple:
      - ("Escalate", "<reason>") if any condition is met
      - ("AI Resolved", None) otherwise
    
    Escalation Conditions:
      1. priority == "Critical"
      2. ai_confidence < 0.70
      3. resolution_success == False
      4. customer_requested_human == True
      5. repeated_attempts >= 3
    """
    priority = ticket_data.get("priority", "")
    ai_confidence = ticket_data.get("ai_confidence", 1.0)
    resolution_success = ticket_data.get("resolution_success", True)
    customer_requested_human = ticket_data.get("customer_requested_human", False)
    repeated_attempts = ticket_data.get("repeated_attempts", 0)

    if priority == "Critical" or priority == "P1":
        return "Escalate", "Critical priority — immediate human intervention required"

    if ai_confidence < 0.70:
        return "Escalate", f"Low AI confidence ({ai_confidence:.0%}) — below 70% threshold"

    if not resolution_success:
        return "Escalate", "AI resolution was unsuccessful"

    if customer_requested_human:
        return "Escalate", "Customer explicitly requested human support"

    if repeated_attempts >= 3:
        return "Escalate", f"Exceeded retry limit ({repeated_attempts} attempts)"

    return "AI Resolved", None


def get_escalation_summary(tickets):
    """
    Given a list of ticket dicts, return summary statistics.
    """
    total = len(tickets)
    escalated = sum(1 for t in tickets if t.get("status") in ("Escalate", "Escalated"))
    ai_resolved = total - escalated
    return {
        "total": total,
        "escalated": escalated,
        "ai_resolved": ai_resolved,
        "escalation_rate": round((escalated / total * 100) if total else 0, 1),
    }
