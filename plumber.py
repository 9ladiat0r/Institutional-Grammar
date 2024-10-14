import pdfplumber
import re
import csv

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def reformat_text(text):
    pattern = r"(\d+)\s+(.+?)\n(a\)|b\)|c\))(.+?)(?:\n|$)"
    reformatted_lines = []
    
    for match in re.finditer(pattern, text, re.DOTALL):
        num, main_text, _, options = match.groups()
        option_lines = options.split("\n")
        for i, option in enumerate(option_lines):
            reformatted_lines.append(f"{int(num) + i}) {main_text.strip()} {option.strip()}")
    
    return "\n".join(reformatted_lines)

def text_to_csv(reformatted_text, csv_path):
    lines = reformatted_text.split("\n")
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for line in lines:
            writer.writerow([line])

# Example usage
if __name__ == "__main__":
    pdf_path = "/Users/karan/Desktop/3-1/LOP/acts/The Air (Prevention and Control of Pollution) Act of 1981.pdf"
    csv_path = "output.csv"

    text = extract_text_from_pdf(pdf_path)
    reformatted_text = reformat_text(text)
    text_to_csv(reformatted_text, csv_path)