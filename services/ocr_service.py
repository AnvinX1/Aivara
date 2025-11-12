
import os
try:
    import pdfplumber
except ImportError:
    pdfplumber = None
try:
    from PIL import Image
except ImportError:
    Image = None
try:
    import pytesseract
except ImportError:
    pytesseract = None

def extract_text_from_report(file_path: str) -> str:
    """
    Extracts text from a given report file (PDF or image).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Report file not found: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()
    extracted_text = ""

    try:
        if file_extension == '.pdf':
            if pdfplumber is None:
                raise RuntimeError("pdfplumber is not installed. Please install it to process PDF files.")
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted_text += page.extract_text() + "\n"  # FIX: Doubly escape the newline
        elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']:
            if Image is None or pytesseract is None:
                raise RuntimeError("PIL/Pillow and pytesseract are not installed. Please install them to process image files.")
            img = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(img)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        raise RuntimeError(f"Failed to extract text from report: {e}")

    return extracted_text

if __name__ == '__main__':
    # Example usage (requires dummy files or actual files for testing)
    print("To test PDF extraction, please place a real PDF file in the 'services' directory and update the path.")
    print("Example: text = extract_text_from_report('/content/aivara-backend/services/example.pdf')")

    try:
        from PIL import Image, ImageDraw, ImageFont
        dummy_image_path = os.path.join(os.path.dirname(__file__), 'dummy_image.png')
        img = Image.new('RGB', (300, 100), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        try:
            fnt = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 20)
        except IOError:
            fnt = ImageFont.load_default()

        d.text((10,10), "Hemoglobin 14.5 g/dL", font=fnt, fill=(0,0,0))
        d.text((10,40), "WBC: 7.2 x10^3/uL", font=fnt, fill=(0,0,0))
        img.save(dummy_image_path)
        print(f"Created dummy image for OCR testing: {dummy_image_path}")

        print("\\n--- Testing OCR on dummy image ---") # Fixed
        extracted_img_text = extract_text_from_report(dummy_image_path)
        print(f"Extracted Text (Image):\\n{extracted_img_text}") # Fixed

        os.remove(dummy_image_path)
        print(f"Cleaned up {dummy_image_path}")

    except ImportError:
        print("Pillow or ImageDraw/ImageFont not fully available. Skipping dummy image creation.")
    except Exception as e:
        print(f"Could not create or test dummy image due to: {e}")
