import fitz


def convert_pdf_to_text(pdf_file):
    pdf_content = pdf_file.read()
    doc = fitz.open("pdf", pdf_content)
    text = ""
    for page in doc:
        text += page.get_text()

    return text
