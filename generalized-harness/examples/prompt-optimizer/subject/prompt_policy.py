"""Mutable surface: edit response policy only."""

SYSTEM_STYLE = "concise, practical"


def compose_response(user_intent: str) -> str:
    intent = user_intent.lower()

    if "price" in intent or "trial" in intent:
        return (
            "Our monthly price depends on plan tier. "
            "A trial is available for new users; check the pricing page for current monthly details."
        )

    if "refund" in intent:
        return (
            "Our refund policy allows requests within 14 days of purchase, "
            "subject to policy review and eligibility conditions."
        )

    if "api" in intent or "webhook" in intent:
        return (
            "Our API supports webhook events. "
            "Rate limits apply per key and are documented in the API reference."
        )

    return "Please share your exact question and I will answer clearly."
