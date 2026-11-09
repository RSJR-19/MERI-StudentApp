from pypdf import PdfReader

def extract_eaf_text(pdf_path):
    reader = PdfReader(pdf_path)

    extracted_text = []

    for page in reader.pages:
        text = page.extract_text() or ""
        extracted_text.append(text)

    return "\n".join(extracted_text)