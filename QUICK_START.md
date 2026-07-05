# Quick Start - Single File Shopee Invoice Extractor

## 30 Second Setup

### 1. Install
```bash
pip install PyPDF2 --break-system-packages
```

### 2. Run
```bash
python shopee_invoice_extractor.py invoice.pdf output_folder
```

### 3. Done!
JSON file created at: `output_folder/shopee_invoice_YYYY-MM-DD_NNNNNNN.json`

---

## Usage Examples

### Basic
```bash
python shopee_invoice_extractor.py Shopee-TIV-TRSPEMKP00-00000-260619-0004229.pdf
```

### With Output Folder
```bash
python shopee_invoice_extractor.py invoice.pdf ./processed
```

### Full Path
```bash
python shopee_invoice_extractor.py /mnt/user-data/uploads/invoice.pdf /mnt/user-data/outputs
```

---

## What It Does

1. **Reads** Shopee invoice PDF
2. **Extracts** all fields:
   - Invoice number (merged)
   - Invoice date
   - Seller ID & username
   - Subtotal, VAT, Total
   - Amount in words
3. **Outputs** JSON in format:
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
    "total_in_words": "Fourteen Thousand...",
    "currency": "THB"
  }
]
```

---

## Console Output

```
📄 Processing: Shopee-TIV-TRSPEMKP00-00000-260619-0004229.pdf
──────────────────────────────────────────────────────────────

✓ Extraction successful!
✓ Output: /mnt/user-data/outputs/shopee_invoice_2026-06-19_0004229.json

Extracted Data:
──────────────────────────────────────────────────────────────
  Invoice Number: TRSPEMKP00-00000-2600000-260619-0004229
  Invoice Date:   2026-06-19
  Seller ID:      154656171
  Username:       villamarket
  Subtotal (ex-VAT): ฿13,817.76
  VAT (7%):       ฿967.24
  Total (inc-VAT): ฿14,785.00
──────────────────────────────────────────────────────────────
```

---

## Common Issues

### PyPDF2 not installed
```
pip install PyPDF2 --break-system-packages
```

### File not found
Check file path and make sure file exists

### Permission denied on output
Make sure output folder exists and is writable:
```bash
mkdir -p output
chmod 777 output
```

### Wrong invoice format
This tool only works with standard Shopee (Thailand) invoices

---

## For Batch Processing

If you need to process **multiple invoices at once**, use:
```bash
python shopee_batch_processor.py ./invoices_folder -o ./output -w 4
```

---

## For Integration

### Bash Loop
```bash
for pdf in ./invoices/*.pdf; do
    python shopee_invoice_extractor.py "$pdf" ./output
done
```

### Python Script
```python
import subprocess
result = subprocess.run([
    "python", 
    "shopee_invoice_extractor.py", 
    "invoice.pdf", 
    "./output"
], capture_output=True)

if result.returncode == 0:
    print("✓ Success!")
else:
    print("✗ Failed!")
```

---

## Files You Need

- `shopee_invoice_extractor.py` - Main script
- PyPDF2 library - Installed via pip

That's it!

---

**Ready to use?** 🚀

```bash
python shopee_invoice_extractor.py your_invoice.pdf
```
