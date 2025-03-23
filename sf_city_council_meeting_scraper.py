import requests
import os
import time
from bs4 import BeautifulSoup

# URL of the webpage where PDFs are listed
base_url = "https://sfgov.legistar.com/Calendar.aspx"

# Folder to store downloaded PDFs
download_folder = "downloaded_pdfs"
os.makedirs(download_folder, exist_ok=True)

# Function to scrape PDFs from a single page
def scrape_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract and download PDF links
    pdf_links = []
    downloaded_files = set()  # Track filenames to prevent overwriting

    for index, link in enumerate(soup.find_all("a", href=True)):
        if "View.ashx" in link["href"]:  # Look for PDF download links
            pdf_url = f"https://sfgov.legistar.com/{link['href']}"
            pdf_links.append(pdf_url)

            # Generate a unique filename
            pdf_id = pdf_url.split("=")[-1]  # Extract ID from URL
            pdf_name = f"{pdf_id}_{index}.pdf"  # Add index to ensure uniqueness
            pdf_path = os.path.join(download_folder, pdf_name)

            # Download the PDF with error handling
            pdf_response = requests.get(pdf_url, stream=True)
            
            # Check if the response is a valid PDF
            content_type = pdf_response.headers.get("Content-Type", "")
            if "application/pdf" not in content_type:
                print(f"⚠️ Skipping {pdf_url} - Not a valid PDF (Content-Type: {content_type})")
                continue
            
            # Save the PDF only if it's valid
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(pdf_response.content)

            # Verify if the file is not empty
            if os.path.getsize(pdf_path) < 1024:  # Less than 1KB is suspicious
                print(f"⚠️ Deleting {pdf_name} - File is too small (possibly corrupted).")
                os.remove(pdf_path)
            else:
                print(f"✅ Downloaded: {pdf_name}")
                downloaded_files.add(pdf_name)

    return downloaded_files

# Main function to handle pagination
def scrape_all_pages():
    current_page = 1
    while True:
        print(f"\n📄 Scraping page {current_page}...\n")
        page_url = f"{base_url}?Page={current_page}"

        downloaded = scrape_page(page_url)
        if not downloaded:
            print(f"❌ No more valid PDFs found on page {current_page}. Stopping.")
            break
        
        current_page += 1
        time.sleep(3)  # Pause to prevent server overload

# Run the scraper
scrape_all_pages()
