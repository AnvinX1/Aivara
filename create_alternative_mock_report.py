"""
Script to create an alternative mock medical report PDF with different values.
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def create_alternative_mock_report():
    """Create an alternative mock medical report with slightly different values"""
    
    output_path = os.path.join(os.path.dirname(__file__), "mock_medical_report_2.pdf")
    
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "BLOOD TEST REPORT")
    
    # Header information
    c.setFont("Helvetica", 12)
    y = height - 100
    c.drawString(100, y, "Patient Name: Jane Smith")
    y -= 20
    c.drawString(100, y, f"Report Date: {datetime.now().strftime('%Y-%m-%d')}")
    y -= 20
    c.drawString(100, y, "Lab Reference: LAB-2024-002")
    
    # Section header
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "HEMATOLOGY RESULTS")
    y -= 30
    
    # Test results - using different formats to test parser
    c.setFont("Helvetica", 11)
    results = [
        ("Parameter", "Value", "Units", "Normal Range"),
        ("HGB (Hemoglobin)", "13.2", "g/dL", "12.0-17.5"),
        ("WBC Count", "8.5", "x10^3/uL", "4.0-11.0"),
        ("Platelet Count", "320", "x10^3/uL", "150-450"),
        ("RBC Count", "4.8", "x10^6/uL", "4.5-5.9"),
    ]
    
    x_positions = [100, 250, 350, 450]
    
    for row_idx, row in enumerate(results):
        if row_idx == 0:
            c.setFont("Helvetica-Bold", 10)
        else:
            c.setFont("Helvetica", 10)
        
        for col_idx, text in enumerate(row):
            c.drawString(x_positions[col_idx], y, text)
        y -= 20
    
    # Additional information in paragraph format
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(100, y, "Summary:")
    y -= 15
    c.drawString(100, y, "Hemoglobin: 13.2 g/dL - within normal limits")
    y -= 15
    c.drawString(100, y, "White Blood Cells: 8.5 x10^3/uL - normal")
    y -= 15
    c.drawString(100, y, "Platelets: 320 - normal range")
    y -= 15
    c.drawString(100, y, "RBC: 4.8 x10^6/uL - normal")
    
    # Footer
    y = 50
    c.setFont("Helvetica", 8)
    c.drawString(100, y, "Mock report for testing - Alternative values")
    
    c.save()
    print(f"Created alternative mock PDF: {output_path}")
    return output_path

if __name__ == "__main__":
    create_alternative_mock_report()

