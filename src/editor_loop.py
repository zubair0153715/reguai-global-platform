import os
from colorama import Fore, Style, init
from src.strict_scanner import StrictDocumentScanner

init(autoreset=True)

class InteractiveCorrectionSystem:
    def __init__(self, file_path: str, rules: dict):
        self.file_path = file_path
        self.rules = rules

    def start_correction_workflow(self):
        scanner = StrictDocumentScanner(self.rules)

        while True:
            results = scanner.scan_document(self.file_path)
            
            print("\n" + "=" * 70)
            status_color = Fore.GREEN if results["status"] == "APPROVED" else Fore.RED
            print(f" SCAN RESULTS | STATUS: [{status_color}{results['status']}{Style.RESET_ALL}] | ERRORS DETECTED: {results['total_errors']}")
            print("=" * 70)

            if results["status"] == "APPROVED":
                print(Fore.GREEN + f"\n SUCCESS! Document is 100% compliant with {self.rules['agency']} standards!")
                print(Fore.GREEN + " Certificate of Regulatory Compliance Generated Successfully.")
                break

            print(Fore.YELLOW + "\n DETECTED ERRORS & NON-COMPLIANT HIGHLIGHTS:")
            for idx, err in enumerate(results["errors"], 1):
                if err["line"] > 0:
                    print(f"  [{idx}] Line {err['line']} [{Fore.RED}{err['severity']}{Style.RESET_ALL}]: {err['reason']}")
                    print(f"      Text Highlight: \"{Fore.CYAN}{err['text']}{Style.RESET_ALL}\"")
                else:
                    print(f"  [{idx}] Global [{Fore.RED}{err['severity']}{Style.RESET_ALL}]: {err['reason']}")

            print(Fore.WHITE + "\nACTION REQUIRED: Open file, correct highlighted errors, save, and re-scan.")
            user_input = input("\nPress [ENTER] to Re-Scan file after editing, or type 'exit' to quit: ")
            
            if user_input.strip().lower() == 'exit':
                print(Fore.RED + "Process interrupted. Document is NOT regulatory compliant.")
                break