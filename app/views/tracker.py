# Read from the active textdoc instead of file
textdoc_path = "./GDS_Snippet_Library_Documentation.pdf"

# Create the PDF from the previously defined document string
from fpdf import FPDF

# Use a minimal font style and page settings
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Copy of the content from the canvas textdoc
doc_content = """
# GOV.UK Design System Snippet Library - Implementation Guide

This guide documents how to use and maintain the AI-powered snippet system for generating HTML using the GOV.UK Design System.

...

For help, contact the AI design tooling team or refer to https://design-system.service.gov.uk.
""".strip().splitlines()

# Add content to PDF
for line in doc_content:
    pdf.multi_cell(0, 10, line.strip())

# Output the final PDF
pdf.output(textdoc_path)
textdoc_path
