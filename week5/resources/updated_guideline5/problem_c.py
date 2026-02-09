from decimal import Decimal

def transfer(src, dst, amount: Decimal, ledger, txlog, limits):
    # Section 1: validate + derive authorization state
    if amount <= 0:
        raise ValueError("amount must be positive")
    if src.id == dst.id:
        raise ValueError("self-transfer forbidden")

    risk_flag = amount > limits.instant_threshold
    requires_2fa = risk_flag or src.is_new_device

    # soft reserve starts here and must be released on all exits
    hold_id = ledger.place_hold(src.id, amount)

    # Section 2: fraud + policy checks
    if ledger.daily_outgoing(src.id) + amount > limits.daily_cap:
        ledger.release_hold(hold_id)
        return {"ok": False, "reason": "daily_cap"}

    if requires_2fa and not src.session.has_2fa:
        ledger.release_hold(hold_id)
        return {"ok": False, "reason": "2fa_required"}

    # Section 3: commit + audit
    try:
        ledger.debit(src.id, amount)
        ledger.credit(dst.id, amount)
        tx_id = txlog.record(
            src=src.id, dst=dst.id, amount=str(amount), risk=risk_flag
        )
        ledger.release_hold(hold_id)
        return {"ok": True, "tx_id": tx_id, "risk": risk_flag}
    except Exception:
        ledger.release_hold(hold_id)
        raise
