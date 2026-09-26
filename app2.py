import os
import time
from google import genai
from google.genai import types
import pymupdf
from config import API_KEY, SOURCE_FOLDER, TARGET_FOLDER

# 1. Initialize GenAI client
client = genai.Client(api_key=API_KEY)

# Ensure the target output folder exists
os.makedirs(TARGET_FOLDER, exist_ok=True)

# 2. Find all PDF files in the source folder
pdf_files = [f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith(".pdf")]

if not pdf_files:
    print(f"No PDF files found in: {SOURCE_FOLDER}")
else:
    print(f"Found {len(pdf_files)} PDF file(s) to process.")

    # 3. Process each PDF file found in the folder
    for pdf_file in pdf_files:
        input_pdf = os.path.join(SOURCE_FOLDER, pdf_file)
        
        # Create a matching text file name (e.g., "test.pdf" becomes "test.txt")
        base_name = os.path.splitext(pdf_file)[0]
        output_txt = os.path.join(TARGET_FOLDER, f"{base_name}_transcription.txt")

        print(f"\n--- Starting file: {pdf_file} ---")
        
        doc = pymupdf.open(input_pdf)
        total_pages = len(doc)
        print(f"Total pages to process: {total_pages}")

        with open(output_txt, "w", encoding="utf-8") as out_file:
            for i, page in enumerate(doc, start=1):
                print(f"\nProcessing page {i} of {total_pages}...")

                # Render PDF page to PNG bytes
                pix = page.get_pixmap(dpi=150)
                image_bytes = pix.tobytes("png")

                try:
                    # Package image bytes correctly using types.Part
                    image_part = types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/png",
                    )

                    # Call API
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=[
                            image_part,
                            "Transcribe and extract all text from this page accurately, preserving reading order.",
                        ],
                    )

                    page_text = response.text or ""

                    # Terminal preview
                    print(f"--- Page {i} Preview ---")
                    print(page_text[:200] + ("..." if len(page_text) > 200 else ""))

                    # Save to output file
                    out_file.write(f"=== PAGE {i} ===\n\n")
                    out_file.write(page_text)
                    out_file.write("\n\n" + "=" * 20 + "\n\n")

                except Exception as e:
                    error_msg = f"Error processing page {i}: {e}"
                    print(error_msg)
                    out_file.write(f"=== PAGE {i} ===\n\n{error_msg}\n\n")

                # ==========================================================
                # RATE LIMIT THROTTLE: Slows down queries to protect free tier
                # Set to True to enable the pause, False to disable completely.
                # ==========================================================
                ENABLE_THROTTLE = True  
                THROTTLE_SECONDS = 4.0  # Adjust seconds between pages if needed
                
                if ENABLE_THROTTLE:
                    time.sleep(THROTTLE_SECONDS)

        print(f"Finished! Saved to: {output_txt}")

print("\nAll batch processing complete!")