import os
from groq import Groq

class RegulatoryAIFixer:
    """Uses Groq Llama-3 to automatically rewrite non-compliant text into compliant regulatory phrasing."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def auto_fix_text(self, document_text: str, agency_name: str, errors: list) -> str:
        if not self.client:
            return document_text  # Fallback if no API key

        prompt = f"""
        You are an expert Regulatory Affairs Specialist.
        Rewrite the following medical/pharma document text so that it completely complies with {agency_name} regulations.
        
        Current Compliance Violations:
        {errors}
        
        Original Document Text:
        \"\"\"{document_text}\"\"\"
        
        Instructions:
        1. Remove all restricted terms (e.g., 'guaranteed cure', '100% safe').
        2. Insert any missing mandatory statutory sections/keywords required by {agency_name}.
        3. Output ONLY the fully revised compliant document text. Do not include commentary.
        """

        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1
        )
        return response.choices[0].message.content.strip()