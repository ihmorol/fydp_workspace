from PyPDF2 import PdfReader

reader = PdfReader(r'd:\United International University\11th Trimester\FYDP\fydp_workspace\paper1.pdf')
with open(r'd:\United International University\11th Trimester\FYDP\fydp_workspace\paper1_text.txt', 'w', encoding='utf-8') as f:
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        f.write(f"\n=== PAGE {i+1} ===\n")
        f.write(text if text else "[No text extracted]")
print("Done")
