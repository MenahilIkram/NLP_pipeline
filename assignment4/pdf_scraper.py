"""
auto_download_50_pdfs.py
--------------------------
Fully automatic. Downloads 10 articles each for 5 categories (50 PDFs
total) from Wikipedia and saves them as real PDF files, organised into
category folders. Nothing to edit -- just install the 2 packages and run.

STEP 1 (run once in your terminal):
    pip install requests reportlab

STEP 2:
    python auto_download_50_pdfs.py
"""

import os
import re
import time
import requests
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

OUT_DIR = "data/pdfs"
DELAY_SECONDS = 1.0
HEADERS = {"User-Agent": "AcademicCorpusBot/1.0 (coursework; contact: student@example.com)"}

# 5 categories x 10 real Wikipedia article titles = 50 PDFs
CATEGORIES = {
    "Sports": ["Cricket", "Association football", "Basketball", "Tennis", "Olympic Games",
               "Boxing", "Field hockey", "Marathon", "Badminton", "Rugby football"],
    "Technology": ["Artificial intelligence", "Cloud computing", "Computer security",
                   "Machine learning", "Internet of things", "Blockchain", "Robotics",
                   "5G", "Quantum computing", "Software engineering"],
    "Health": ["Nutrition", "Mental health", "Vaccine", "Public health",
               "Cardiovascular disease", "Exercise", "Obesity", "Diabetes",
               "Epidemiology", "Medicine"],
    "Finance": ["Stock market", "Inflation", "Central bank", "Cryptocurrency",
                "Investment", "Insurance", "Bank", "Personal finance",
                "Economic growth", "Taxation"],
    "Education": ["Higher education", "Distance education", "Curriculum", "Literacy",
                  "Educational technology", "Vocational education", "Special education",
                  "Education policy", "Scholarship", "Standardized test"],
}


def fetch_wikipedia_text(title):
    """Fetch the plain-text extract of a Wikipedia article via the official API."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": 1,
        "titles": title,
        "format": "json",
        "redirects": 1,
    }
    resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    pages = resp.json()["query"]["pages"]
    page = next(iter(pages.values()))
    return page.get("extract", "").strip()


def safe_filename(text):
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return text[:40] if text else "article"


def save_as_pdf(title, text, save_path):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(save_path, pagesize=A4)
    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]
    for para in text.split("\n"):
        para = para.strip()
        if len(para) > 20:  # skip empty lines / bare section headers
            story.append(Paragraph(para, styles["Normal"]))
            story.append(Spacer(1, 8))
    doc.build(story)


def main():
    total = 0
    for category, titles in CATEGORIES.items():
        cat_dir = os.path.join(OUT_DIR, category)
        os.makedirs(cat_dir, exist_ok=True)
        print(f"\n=== {category} ===")

        for i, title in enumerate(titles, start=1):
            try:
                text = fetch_wikipedia_text(title)
                if len(text) < 200:
                    print(f"  [{i:02d}] '{title}' -> too short, skipped")
                    continue
                fname = f"{category.lower()}_{i:02d}_{safe_filename(title)}.pdf"
                save_path = os.path.join(cat_dir, fname)
                save_as_pdf(title, text, save_path)
                print(f"  [{i:02d}] Saved -> {save_path}")
                total += 1
                time.sleep(DELAY_SECONDS)
            except Exception as e:
                print(f"  [{i:02d}] Failed on '{title}': {e}")

    print(f"\nDONE. Total PDFs downloaded and saved: {total}")
    print(f"Check the folder: {OUT_DIR}/")


if __name__ == "__main__":
    main()