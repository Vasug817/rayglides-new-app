import os
import csv
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'RayGlides EV Kit Cooling Controller Design File', new_x="LMARGIN", new_y="NEXT", align='L')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def clean_text(text):
    text = text.replace('—', '-')
    text = text.replace('–', '-')
    text = text.replace('°', ' deg ')
    text = text.replace('µ', 'u')
    text = text.replace('²', '^2')
    text = text.replace('…', '...')
    text = text.replace('±', '+/-')
    return text.encode('latin1', 'replace').decode('latin1')

def convert_md_to_pdf(md_path, pdf_path):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_margins(15, 20, 15)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    in_code = False
    code_text = []
    
    for line in lines:
        cleaned_line = clean_text(line)
        stripped = cleaned_line.strip()
        
        # Code block tracking
        if stripped.startswith('```'):
            if in_code:
                in_code = False
                pdf.set_font('Courier', '', 8)
                pdf.set_fill_color(240, 240, 240)
                full_code = '\n'.join(code_text)
                pdf.multi_cell(0, 4, full_code, border=1, fill=True)
                pdf.ln(5)
                code_text = []
            else:
                in_code = True
            continue
            
        if in_code:
            code_text.append(cleaned_line.rstrip('\n'))
            continue
            
        # Headers
        if stripped.startswith('# '):
            pdf.set_font('Helvetica', 'B', 16)
            pdf.set_text_color(31, 78, 121) # Deep Blue
            pdf.multi_cell(0, 10, stripped[2:])
            pdf.ln(5)
        elif stripped.startswith('## '):
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(46, 116, 181)
            pdf.multi_cell(0, 8, stripped[3:])
            pdf.ln(4)
        elif stripped.startswith('### '):
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 6, stripped[4:])
            pdf.ln(3)
        # Lists
        elif stripped.startswith('* ') or stripped.startswith('- '):
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(50, 50, 50)
            pdf.write(5, '   *  ')
            text = stripped[2:]
            pdf.multi_cell(0, 5, text)
            pdf.ln(1)
        elif stripped.startswith('1. ') or stripped.startswith('2. ') or stripped.startswith('3. ') or stripped.startswith('4. ') or stripped.startswith('5. '):
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, '   ' + stripped)
            pdf.ln(1)
        # Table Parsing
        elif stripped.startswith('|') and not stripped.startswith('| :---'):
            parts = [p.strip() for p in stripped.split('|')[1:-1]]
            if len(parts) > 1:
                pdf.set_font('Helvetica', 'B' if 'Net' in stripped or 'Ref' in stripped or 'Parameter' in stripped else '', 8)
                pdf.set_text_color(0, 0, 0)
                col_width = (pdf.epw) / len(parts)
                for part in parts:
                    pdf.cell(col_width, 6, part, border=1)
                pdf.ln(6)
        # Normal paragraphs
        else:
            if stripped == "":
                pdf.ln(2)
                continue
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, stripped)
            pdf.ln(3)
            
    pdf.output(pdf_path)

def convert_csv_to_pdf(csv_path, pdf_path):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_margins(10, 20, 10)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(31, 78, 121)
    pdf.cell(0, 10, 'RayGlides Cooling Controller - Complete Bill of Materials (BOM)', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
    for i, row in enumerate(rows):
        if i == 0:
            pdf.set_font('Helvetica', 'B', 7)
            pdf.set_fill_color(220, 220, 220)
        else:
            pdf.set_font('Helvetica', '', 6)
            pdf.set_fill_color(255, 255, 255)
            
        # Define manual column widths to fit on page (Total width = 190)
        widths = [8, 25, 25, 22, 28, 17, 7, 58]
        
        for j, val in enumerate(row):
            cleaned_val = clean_text(val)
            w = widths[j] if j < len(widths) else 20
            if j == 7:
                pdf.multi_cell(w, 5, cleaned_val, border=1, fill=True)
            else:
                pdf.cell(w, 5, cleaned_val, border=1, fill=True)
        pdf.ln(5)
        
    pdf.output(pdf_path)

# Scan Desktop project folders and compile
root_dir = "/Users/vasugupta/Desktop/rayglides_ev_kit_cooling_controller"
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        full_path = os.path.join(dirpath, filename)
        if filename.endswith('.md'):
            pdf_filename = filename[:-3] + '.pdf'
            pdf_path = os.path.join(dirpath, pdf_filename)
            print(f"Converting MD: {filename} -> {pdf_filename}")
            try:
                convert_md_to_pdf(full_path, pdf_path)
            except Exception as e:
                print(f"Error converting {filename}: {e}")
        elif filename.endswith('.csv'):
            pdf_filename = filename[:-4] + '.pdf'
            pdf_path = os.path.join(dirpath, pdf_filename)
            print(f"Converting CSV: {filename} -> {pdf_filename}")
            try:
                convert_csv_to_pdf(full_path, pdf_path)
            except Exception as e:
                print(f"Error converting {filename}: {e}")
