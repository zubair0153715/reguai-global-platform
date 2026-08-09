import sys
import os
from src.country_rules import CountryRulesEngine
from src.editor_loop import InteractiveCorrectionSystem

def main():
    print("=================================================================")
    print("   ENTERPRISE MULTI-COUNTRY REGULATORY AUDITOR & CORRECTOR V3   ")
    print("=================================================================")

    print("\nSelect Target Regulatory Authority:")
    print("1. US-FDA (United States)")
    print("2. EU-EMA (European Union)")
    print("3. PK-DRAP (Pakistan)")
    
    choice = input("\nEnter Option Number (1-3) [Default 1]: ").strip()
    country_map = {"1": "US_FDA", "2": "EU_EMA", "3": "PK_DRAP"}
    selected_country = country_map.get(choice, "US_FDA")
    
    rules = CountryRulesEngine.get_rules(selected_country)
    print(f"\n Active Authority Loaded: {rules['agency']}")

    doc_path = input("\nEnter Path of Document to Scan (or press Enter for default sample): ").strip()
    if not doc_path:
        doc_path = "sample_submission.txt"
        with open(doc_path, "w") as f:
            f.write("Drug Evaluation Report\nThis product is a guaranteed cure with 100% safe results.\nMissing details here.")

    corrector = InteractiveCorrectionSystem(doc_path, rules)
    corrector.start_correction_workflow()

if __name__ == "__main__":
    main()