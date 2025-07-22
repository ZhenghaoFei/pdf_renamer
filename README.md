# PDF Renamer

This Python script renames PDF files in a specified folder based on the title found on the first page of each PDF. It uses a small Large Language Model (LLM) to extract the title from the text.

## Setup

1.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Place PDFs:**

    Put the PDF files you want to rename into the `pdfs` directory.

## Usage

To run the script, execute the following command from the `pdf_renamer` directory, replacing `pdfs` with the path to your folder if it's different:

```bash
python rename_pdfs.py pdfs
```

## How it Works

-   The script iterates through each PDF file in the specified folder.
-   It reads the text from the first page of the PDF.
-   It uses the `deepset/minilm-uncased-squad2` model to find the title in the text.
-   It sanitizes the title to create a valid filename.
-   It renames the PDF file with the new title.
