# AGENTS.md

## Project overview

This repository contains a single-file Python CLI for extracting structured JSON
from Shopee (Thailand) tax-invoice PDFs and SPX Express receipt PDFs.

- Entrypoint: `shopee_invoice_extractor.py`
- Runtime dependencies: `requirements.txt` (`PyPDF2`, `python-dotenv`)
- User-facing usage notes: `QUICK_START.md` and
  `SINGLE_FILE_EXTRACTOR_README.md`
- There is currently no automated test suite or formatter/linter configuration.

## Setup and verification

Use Python 3.8+ and install the pinned dependencies:

```powershell
python -m pip install -r requirements.txt
```

Before handing off Python changes, at minimum check syntax:

```powershell
python -m py_compile shopee_invoice_extractor.py
```

For a manual extraction check, always provide an explicit PDF and a disposable
output directory:

```powershell
python shopee_invoice_extractor.py <invoice.pdf> <output-dir>
```

Do **not** run the script without arguments during routine verification. That
mode reads `DOWNLOAD_FOLDER` from `.env`, deletes existing `processed/*.json`
and `output.json`, moves successfully processed PDFs into `inserted/`, and then
creates a combined `output.json`.

## Implementation notes

- `ShopeeInvoiceExtractor` handles standard Shopee invoices.
- `SPXReceiptExtractor` handles filenames beginning with `SPX Express-RCT`;
  retain this routing rule in `create_extractor` when extending document
  handling.
- Extraction is regex-based over text from `PyPDF2.PdfReader`. Keep parsing
  tolerant: unavailable optional fields should remain empty or absent according
  to the existing extractor behavior, while `invoice_number` and
  `invoice_date` are required for a successful extraction.
- JSON output is a one-element array per source PDF. Folder-processing mode
  combines those arrays into `output.json`.
- Preserve UTF-8 output and `ensure_ascii=False`, because invoice content may
  include Thai text.

## Change guidelines

- Keep the script usable from Windows PowerShell as documented above.
- Do not expose or commit `.env` values. `DOWNLOAD_FOLDER` is environment-local.
- Do not commit generated PDFs, extracted JSON, `inserted/`, `processed/`,
  `output.json`, or Python cache files; JSON is intentionally ignored by this
  repository.
- When changing CLI behavior or output fields, update both README files so the
  examples and schema stay accurate.
- Avoid unrelated refactors in this small single-file project. Add focused
  tests before making high-risk changes to parsing rules or destructive folder
  processing.
