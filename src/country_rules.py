import json

class CountryRulesEngine:
    RULES_DATA = {
        "US_FDA": {
            "agency": "US Food and Drug Administration (FDA)",
            "required_keywords": ["Adverse Event", "CMC Batch Analysis", "IND Protocol"],
            "restricted_terms": ["guaranteed cure", "100% safe", "unverified efficacy"]
        },
        "EU_EMA": {
            "agency": "European Medicines Agency (EMA)",
            "required_keywords": ["Qualified Person", "SmPC", "EudraVigilance"],
            "restricted_terms": ["guaranteed cure", "unverified efficacy"]
        },
        "PK_DRAP": {
            "agency": "Drug Regulatory Authority of Pakistan (DRAP)",
            "required_keywords": ["Form 5 Registration", "GMP Certificate", "Stability Data Zone IVb"],
            "restricted_terms": ["unregistered batch", "guaranteed cure"]
        }
    }

    @classmethod
    def get_rules(cls, country_code: str):
        return cls.RULES_DATA.get(country_code, cls.RULES_DATA["US_FDA"])