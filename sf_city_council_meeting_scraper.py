"""import requests

# URL of the PDF
pdf_url = "https://sfgov.legistar.com/View.ashx?M=M&ID=1282529&GUID=B25F2597-11C8-4898-BC8C-C9108DFD42AA"

# Send a GET request to fetch the PDF
response = requests.get(pdf_url)

if response.status_code == 200:
    with open("meeting_notes.pdf", "wb") as file:
        file.write(response.content)
    print("PDF downloaded successfully!")
else:
    print("Failed to download PDF:", response.status_code)
"""

"""
import requests
import os
from bs4 import BeautifulSoup

# URL of the webpage where PDFs are listed
website_url = "https://sfgov.legistar.com/Calendar.aspx"

# Folder to store downloaded PDFs
download_folder = "downloaded_pdfs"
os.makedirs(download_folder, exist_ok=True)

# Fetch the webpage content
response = requests.get(website_url)

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Extract and download PDF links
pdf_links = []
for link in soup.find_all("a", href=True):
    if "View.ashx" in link["href"]:  # Look for PDF download links
        pdf_url = f"https://sfgov.legistar.com/{link['href']}"
        pdf_links.append(pdf_url)

        # Generate a filename
        pdf_name = pdf_url.split("=")[-1] + ".pdf"
        pdf_path = os.path.join(download_folder, pdf_name)

        # Download the PDF
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code == 200:
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(pdf_response.content)
            print(f"Downloaded: {pdf_name}")
        else:
            print(f"Failed to download: {pdf_url}")

print("\nAll PDFs downloaded successfully!")
"""

import requests
import os
import time
from bs4 import BeautifulSoup

# URL of the webpage where PDFs are listed
website_url = "https://sfgov.legistar.com/Calendar.aspx"

# Folder to store downloaded PDFs
download_folder = "downloaded_pdfs"
os.makedirs(download_folder, exist_ok=True)

# Fetch the webpage content
response = requests.get(website_url)
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

print(f"\n🎉 Total valid PDFs downloaded: {len(downloaded_files)}")
