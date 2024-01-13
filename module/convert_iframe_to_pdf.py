from weasyprint import HTML

def convert_iframe_to_pdf(source, output_pdf_path):
    HTML(string=source).write_pdf(output_pdf_path)


