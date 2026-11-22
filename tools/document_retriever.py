
import re
from pathlib import Path

from app.config import BASE_DIR, UPLOAD_DIR


POLICY_FILE = BASE_DIR / "data" / "banking_policy.txt"

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


# -----------------------------------------
# 1. Extract text from documents
# -----------------------------------------

def extract_text(file_path):

    file_path = Path(file_path)

    # Check whether file exists
    if not file_path.exists():
        print(f"Skipping missing file: {file_path.name}")
        return ""

    # Check whether it is a file
    if not file_path.is_file():
        print(f"Skipping invalid file: {file_path.name}")
        return ""

    # Skip empty files
    if file_path.stat().st_size == 0:
        print(f"Skipping empty file: {file_path.name}")
        return ""

    suffix = file_path.suffix.lower()

    try:

        # TXT extraction
        if suffix == ".txt":

            return file_path.read_text(
                encoding="utf-8-sig",
                errors="replace"
            )

        # PDF extraction
        elif suffix == ".pdf":

            from pypdf import PdfReader

            reader = PdfReader(str(file_path))

            return "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        # DOCX extraction
        elif suffix == ".docx":

            from docx import Document

            document = Document(str(file_path))

            return "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            )

    except Exception as error:

        print(
            f"Skipping {file_path.name}: {error}"
        )

        return ""

    return ""


# -----------------------------------------
# 2. Get all available documents
# -----------------------------------------

def get_all_documents():

    documents = []

    # Add banking policy TXT
    if POLICY_FILE.is_file():

        documents.append(POLICY_FILE)

    # Add uploaded documents
    if UPLOAD_DIR.exists() and UPLOAD_DIR.is_dir():

        for path in UPLOAD_DIR.iterdir():

            if path.name.startswith("~$"):
                continue

            if (
                path.is_file()
                and path.suffix.lower() in SUPPORTED_EXTENSIONS
            ):

                if path.stat().st_size > 0:

                    documents.append(path)

                else:

                    print(
                        f"Skipping empty file: {path.name}"
                    )

    # Remove duplicate paths
    return list(dict.fromkeys(documents))


# -----------------------------------------
# 3. Search banking policy documents
# -----------------------------------------

def search_policy(query: str, top_k: int = 4):

    if not query or not query.strip():
        return []

    if top_k <= 0:
        return []

    query_words = set(
        re.findall(r"[a-z0-9]+", query.lower())
    )

    results = []

    # Read all available documents
    for file_path in get_all_documents():

        text = extract_text(file_path)

        if not text or not text.strip():
            continue

        # Split document into paragraphs
        paragraphs = [
            paragraph.strip()
            for paragraph in re.split(
                r"\n\s*\n",
                text.replace("\r\n", "\n").replace("\r", "\n")
            )
            if paragraph.strip()
        ]

        # If there are no paragraph breaks,
        # split using individual lines
        if len(paragraphs) == 1:

            lines = [
                line.strip()
                for line in paragraphs[0].split("\n")
                if line.strip()
            ]

            if len(lines) > 1:
                paragraphs = lines

        # Search each paragraph
        for index, paragraph in enumerate(
            paragraphs, start=1
        ):

            words = set(
                re.findall(
                    r"[a-z0-9]+",
                    paragraph.lower()
                )
            )

            score = len(
                query_words.intersection(words)
            )

            if score > 0:

                results.append({

                    "source": file_path.name,

                    "section": index,

                    "score": score,

                    "text": paragraph

                })

    # Sort by relevance score
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]
