import io
import zipfile

class eCTDExporter:
    """Generates eCTD Module 1-5 folder structure with index.xml manifest in a downloadable ZIP."""

    @staticmethod
    def create_ectd_zip(doc_name: str, doc_content: str, country_code: str) -> bytes:
        zip_buffer = io.BytesIO()

        index_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<ectd:ectd xmlns:ectd="http://www.ich.org/ectd" version="3.2.2">
    <header>
        <submission_type>Initial Submission</submission_type>
        <jurisdiction>{country_code}</jurisdiction>
    </header>
    <m1_regional>
        <leaf filename="{doc_name}"/>
    </m1_regional>
</ectd:ectd>
"""

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # eCTD Folder Hierarchy
            zip_file.writestr("m1/regional/index.xml", index_xml)
            zip_file.writestr(f"m1/regional/{doc_name}", doc_content)
            zip_file.writestr("m2/summaries/m2-quality-summary.txt", "eCTD Module 2 Quality Summary Placeholder")
            zip_file.writestr("m3/quality/m3-body-data.txt", "eCTD Module 3 Quality Data Placeholder")
            zip_file.writestr("m4/nonclinical/m4-reports.txt", "eCTD Module 4 Nonclinical Reports")
            zip_file.writestr("m5/clinical/m5-study-reports.txt", "eCTD Module 5 Clinical Study Reports")

        zip_buffer.seek(0)
        return zip_buffer.getvalue()