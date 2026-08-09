class StripeSubscriptionManager:
    """Manages SaaS Tier Upgrades and Billing Links for ReguAI."""
    
    CHECKOUT_URLS = {
        "Pro": "https://buy.stripe.com/test_reguai_pro_plan",
        "Enterprise": "https://buy.stripe.com/test_reguai_enterprise_plan"
    }

    @staticmethod
    def get_tier_features(tier: str = "Free"):
        if tier == "Pro":
            return {
                "max_scans": "Unlimited",
                "ai_autofix": True,
                "pdf_cert": True,
                "ectd_export": False,
                "api_access": False
            }
        elif tier == "Enterprise":
            return {
                "max_scans": "Unlimited",
                "ai_autofix": True,
                "pdf_cert": True,
                "ectd_export": True,
                "api_access": True
            }
        else: # Free Tier
            return {
                "max_scans": 3,
                "ai_autofix": False,
                "pdf_cert": True,
                "ectd_export": False,
                "api_access": False
            }