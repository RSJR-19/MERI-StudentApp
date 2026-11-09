from pypdf import PdfReader

def extract_pdf(file_path):
    reader = PdfReader(file_path)

    extracted_text = ""

    for page in reader.pages:
        extracted_text += page.extract_text() or ""

    return extracted_text


print(extract_pdf("app/services/EAF.pdf"))