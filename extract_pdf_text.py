import fitz  # PyMuPDF
import os

source_dir = r"d:\United International University\11th Trimester\FYDP\fydp_workspace\All papers"
output_dir = r"d:\United International University\11th Trimester\FYDP\fydp_workspace\All Paper txt"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

pdf_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.pdf')]
pdf_files.sort()

print(f"Found {len(pdf_files)} PDF files to process.\n")

for idx, pdf_name in enumerate(pdf_files, 1):
    pdf_path = os.path.join(source_dir, pdf_name)
    # Create output filename: original name (without .pdf) + _text.txt
    base_name = os.path.splitext(pdf_name)[0]
    output_name = f"{base_name}_text.txt"
    output_path = os.path.join(output_dir, output_name)

    print(f"[{idx}/{len(pdf_files)}] Processing: {pdf_name}")

    try:
        doc = fitz.open(pdf_path)
        all_text = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            all_text.append(f"\n=== PAGE {page_num + 1} ===\n{text}")

        doc.close()

        # Write to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(all_text))

        print(f"    -> Saved: {output_name}")

    except Exception as e:
        print(f"    -> ERROR: {e}")

print(f"\nDone! All text files saved to: {output_dir}")
