import sys

file_path = "e:\\University\\FYDP\\resources\\fydp-1-proposal (1).pdf"

try:
    import fitz # PyMuPDF
    doc = fitz.open(file_path)
    with open("pdf_text.txt", "w", encoding="utf-8") as f:
        for i, page in enumerate(doc):
            f.write(f"--- PAGE {i+1} ---\n")
            f.write(page.get_text() + "\n")
except Exception as e:
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        with open("pdf_text.txt", "w", encoding="utf-8") as f:
            for i, page in enumerate(reader.pages):
                f.write(f"--- PAGE {i+1} ---\n")
                f.write(page.extract_text() + "\n")
    except Exception as e2:
        import traceback
        traceback.print_exc()
        print(f"Error1: {e}\nError2: {e2}")
