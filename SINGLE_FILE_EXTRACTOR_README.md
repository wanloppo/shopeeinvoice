# Shopee Invoice Extractor - Single File

Simple Python script to extract data from a single Shopee invoice PDF and convert to JSON.

## Features

✅ **Single File Processing** - Extract one invoice at a time  
✅ **Simple CLI** - Easy to use command-line interface  
✅ **JSON Array Format** - Output as `[{ ... }]`  
✅ **Error Handling** - Graceful error messages  
✅ **Fast** - Process in 1-2 seconds  

## Installation

### Requirements

```bash
pip install PyPDF2 --break-system-packages
```

### File

```
shopee_invoice_extractor.py
```

## Usage

### Basic Usage

```bash
python3 shopee_invoice_extractor.py <pdf_file>
```

### With Output Directory

```bash
python3 shopee_invoice_extractor.py <pdf_file> <output_dir>
```

## Examples

### Example 1: Process single invoice in current directory

```bash
python3 shopee_invoice_extractor.py Shopee-TIV-TRSPEMKP00-00000-260619-0004229.pdf
```

**Output:**
- JSON file: `shopee_invoice_2026-06-19_0004229.json` (in same directory as script)

### Example 2: Specify output directory

```bash
python3 shopee_invoice_extractor.py invoice.pdf ./output
```

**Output:**
- JSON file: `./output/shopee_invoice_2026-06-19_0004229.json`

### Example 3: Batch processing with loop

```bash
# Process all Shopee invoices in a directory
for pdf in *.pdf; do
    python3 shopee_invoice_extractor.py "$pdf" ./processed
done
```

### Example 4: Store in variable (Python integration)

```python
import subprocess
import json

pdf_file = "invoice.pdf"
result = subprocess.run(
    ["python3", "shopee_invoice_extractor.py", pdf_file, "./output"],
    capture_output=True
)

if result.returncode == 0:
    # Read the generated JSON
    with open("./output/shopee_invoice_2026-06-19_0004229.json") as f:
        data = json.load(f)
    print(f"Invoice: {data[0]['invoice_number']}")
    print(f"Amount: ฿{data[0]['total_with_vat']:,.2f}")
```

## Output Format

### JSON Array with Single Object

```json
[
  {
    "invoice_number": "TRSPEMKP00-00000-2600000-260619-0004229",
    "invoice_date": "2026-06-19",
    "seller_id": "154656171",
    "seller_username": "villamarket",
    "subtotal_before_vat": 13817.76,
    "discount": 0.0,
    "subtotal_after_discount": 13817.76,
    "vat_amount": 967.24,
    "vat_rate_percent": 7.0,
    "total_with_vat": 14785.0,
    "total_in_words": "Fourteen Thousand, Seven Hundred And Eighty-Five Baht",
    "currency": "THB"
  }
]
```

## Field Description

| Field | Type | Description |
|-------|------|-------------|
| `invoice_number` | string | Merged invoice + reference ID |
| `invoice_date` | string | Invoice date (YYYY-MM-DD) |
| `seller_id` | string | Shopee seller ID |
| `seller_username` | string | Seller's Shopee username |
| `subtotal_before_vat` | float | Line items total before VAT |
| `discount` | float | Discount amount |
| `subtotal_after_discount` | float | Total after discount |
| `vat_amount` | float | VAT amount (7%) |
| `vat_rate_percent` | float | VAT rate percentage |
| `total_with_vat` | float | Final total including VAT |
| `total_in_words` | string | Amount in English words |
| `currency` | string | Currency code (THB) |

## Console Output

When you run the script, you'll see:

```
📄 Processing: Shopee-TIV-TRSPEMKP00-00000-260619-0004229.pdf
──────────────────────────────────────────────────────────────────────

✓ Extraction successful!
✓ Output: /mnt/user-data/outputs/shopee_invoice_2026-06-19_0004229.json

Extracted Data:
──────────────────────────────────────────────────────────────────────
  Invoice Number: TRSPEMKP00-00000-2600000-260619-0004229
  Invoice Date:   2026-06-19
  Seller ID:      154656171
  Username:       villamarket
  Subtotal (ex-VAT): ฿13,817.76
  VAT (7%):       ฿967.24
  Total (inc-VAT): ฿14,785.00
──────────────────────────────────────────────────────────────────────
```

## Error Messages

### File Not Found
```
✗ Error: File not found - invoice.pdf
```

**Solution:** Verify file path and name are correct

### PyPDF2 Not Installed
```
ERROR: PyPDF2 not installed. Install with: pip install PyPDF2
```

**Solution:** Install with pip

### Missing Key Fields
```
✗ Error: Missing key fields (invoice_number or invoice_date)
```

**Solution:** Verify PDF is a valid Shopee invoice

### Read-Only File System
```
✗ Error: Failed to save JSON - [Errno 30] Read-only file system
```

**Solution:** Specify an output directory: `python3 script.py invoice.pdf ./output`

## Exit Codes

- `0` - Success
- `1` - Failure

Useful for shell scripts:

```bash
python3 shopee_invoice_extractor.py invoice.pdf && echo "Success!" || echo "Failed!"
```

## Integration Examples

### Shell Script Loop

```bash
#!/bin/bash
# Process multiple invoices

for pdf in ./invoices/*.pdf; do
    echo "Processing: $pdf"
    python3 shopee_invoice_extractor.py "$pdf" ./output
    if [ $? -eq 0 ]; then
        echo "✓ Success"
    else
        echo "✗ Failed"
    fi
done
```

### Python Integration

```python
import json
import subprocess
from pathlib import Path

pdf_file = "Shopee-TIV-TRSPEMKP00-00000-260619-0004229.pdf"
output_dir = "./processed"

# Run extractor
result = subprocess.run(
    ["python3", "shopee_invoice_extractor.py", pdf_file, output_dir],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    # Read generated JSON
    json_file = Path(output_dir) / "shopee_invoice_2026-06-19_0004229.json"
    with open(json_file) as f:
        invoices = json.load(f)
    
    for invoice in invoices:
        print(f"Invoice: {invoice['invoice_number']}")
        print(f"Amount: ฿{invoice['total_with_vat']:,.2f}")
else:
    print("Extraction failed:")
    print(result.stdout)
```

### Import to MSSQL

```python
import json
import subprocess
import pyodbc

pdf_file = "invoice.pdf"
output_dir = "./output"

# Extract
subprocess.run(["python3", "shopee_invoice_extractor.py", pdf_file, output_dir])

# Import to database
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=villadw;...')
cursor = conn.cursor()

with open(f"{output_dir}/shopee_invoice_2026-06-19_0004229.json") as f:
    invoices = json.load(f)

for invoice in invoices:
    cursor.execute('''
        INSERT INTO ShopeeInvoices 
        (InvoiceNumber, InvoiceDate, SellerId, SellerUsername, TotalWithVAT)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        invoice['invoice_number'],
        invoice['invoice_date'],
        invoice['seller_id'],
        invoice['seller_username'],
        invoice['total_with_vat']
    ))

conn.commit()
print(f"Imported {len(invoices)} invoice(s)")
```

## Performance

- **Processing Time:** 1-2 seconds per invoice
- **Output Size:** ~500 bytes per JSON file
- **Memory Usage:** ~50 MB

## Requirements

- **Python:** 3.8+
- **PyPDF2:** For PDF text extraction
- **Input:** Standard Shopee (Thailand) tax invoice PDF
- **Output:** `[{ }]` formatted JSON

## Supported Invoice Type

- **Merchant:** Shopee (Thailand) Co., Ltd.
- **Invoice Type:** Receipt/Tax Invoice (ใบเสร็จรับเงิน/ใบกำกับภาษี)
- **Language:** Thai/English mixed
- **Template:** Standard Shopee invoice format

## Tips

1. **Batch Processing:** Use the batch processor (`shopee_batch_processor.py`) for multiple files
2. **Error Handling:** Check console output for warnings (marked with ⚠)
3. **Output Naming:** File names are auto-generated from `invoice_date_refnumber`
4. **Script Location:** Can run from any directory
5. **Relative Paths:** Both input and output support relative paths

## Troubleshooting

### Q: Script not found
A: Make executable: `chmod +x shopee_invoice_extractor.py`

### Q: Import errors
A: Reinstall PyPDF2: `pip install --upgrade PyPDF2 --break-system-packages`

### Q: Permission denied
A: Ensure output directory is writable: `mkdir -p output && chmod 777 output`

### Q: Wrong invoice detected
A: Verify the PDF is a Shopee invoice; other invoice types are not supported

## Version History

- **1.0** - Initial release, single file extraction with [{ }] format

---

**Author:** Shopee Invoice Processor  
**Last Updated:** 2026-07-04  
**License:** MIT
