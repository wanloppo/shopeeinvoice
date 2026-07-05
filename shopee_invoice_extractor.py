#!/usr/bin/env python3
"""
Shopee Invoice Extractor - Single File
Extract data from a single Shopee invoice PDF and output as JSON [{ }]
"""

import json
import os
import re
import shutil
import sys
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

try:
    from PyPDF2 import PdfReader
except ImportError:
    print("ERROR: PyPDF2 not installed. Install with: pip install PyPDF2")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("ERROR: python-dotenv not installed. Install with: pip install python-dotenv")
    sys.exit(1)


class ShopeeInvoiceExtractor:
    """Extract and parse single Shopee invoice PDF"""

    def __init__(self, pdf_path: str, output_dir: str = None):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir) if output_dir else self.pdf_path.parent
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.text = ""
        self.data = {}

    def extract_text(self) -> bool:
        """Extract text from PDF"""
        try:
            if not self.pdf_path.exists():
                print(f"✗ Error: File not found - {self.pdf_path}")
                return False
            
            reader = PdfReader(str(self.pdf_path))
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            self.text = text
            return True
        except Exception as e:
            print(f"✗ Error: Failed to extract PDF text - {e}")
            return False

    def extract_invoice_number(self) -> str:
        """Extract and merge invoice number + reference number"""
        try:
            invoice_match = re.search(r'(TRSPEMKP\d{2}-\d{5}-\d{2})', self.text)
            date_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', self.text)
            ref_match = re.search(r'TRSPEMKP\d{2}-\d{5}-\d{2}[^\d]*(\d{4})-(\d{7})', self.text, re.DOTALL)
            
            if invoice_match and date_match and ref_match:
                inv_num = invoice_match.group(1)
                day, month, year = date_match.groups()
                ref_num = ref_match.group(2)
                inv_parts = inv_num.split('-')
                date_str = f"{year[-2:]}{month}{day}"
                merged = f"{inv_parts[0]}-{inv_parts[1]}-{inv_parts[2]}00000-{date_str}-{ref_num}"
                return merged
            
            pattern = r'(TRSPEMKP[\d\-]+)'
            match = re.search(pattern, self.text)
            return match.group(1) if match else ""
        except Exception as e:
            print(f"⚠ Warning: Error extracting invoice number - {e}")
            return ""

    def extract_invoice_date(self) -> str:
        """Extract invoice date in YYYY-MM-DD format"""
        try:
            pattern = r'(\d{2})/(\d{2})/(\d{4})'
            match = re.search(pattern, self.text)
            if match:
                day, month, year = match.groups()
                return f"{year}-{month}-{day}"
            return ""
        except Exception as e:
            print(f"⚠ Warning: Error extracting date - {e}")
            return ""

    def extract_seller_id(self) -> str:
        """Extract Seller ID"""
        try:
            pattern = r'Seller ID\s+(\d+)'
            match = re.search(pattern, self.text)
            return match.group(1) if match else ""
        except Exception as e:
            print(f"⚠ Warning: Error extracting seller ID - {e}")
            return ""

    def extract_seller_username(self) -> str:
        """Extract seller username"""
        try:
            pattern = r'Username\s+(\w+)'
            match = re.search(pattern, self.text)
            return match.group(1) if match else ""
        except Exception as e:
            print(f"⚠ Warning: Error extracting seller username - {e}")
            return ""

    def extract_totals(self) -> Dict[str, Any]:
        """Extract all totals from invoice"""
        totals = {}
        try:
            pattern = r'Total Value of Services \(Excluded VAT\)\s+([\d,]+\.?\d*)'
            match = re.search(pattern, self.text)
            if match:
                totals['subtotal_before_vat'] = float(match.group(1).replace(',', ''))

            pattern = r'Discount\s+([\d,]+\.?\d*)'
            match = re.search(pattern, self.text)
            if match:
                totals['discount'] = float(match.group(1).replace(',', ''))

            pattern = r'after discount\s+([\d,]+\.?\d*)'
            match = re.search(pattern, self.text)
            if match:
                totals['subtotal_after_discount'] = float(match.group(1).replace(',', ''))

            pattern = r'VAT 7%\s+([\d,]+\.?\d*)'
            match = re.search(pattern, self.text)
            if match:
                totals['vat_amount'] = float(match.group(1).replace(',', ''))
                totals['vat_rate_percent'] = 7.0

            pattern = r'Total Value of Services \(Included VAT\)\s+([\d,]+\.?\d*)'
            match = re.search(pattern, self.text)
            if match:
                totals['total_with_vat'] = float(match.group(1).replace(',', ''))

            pattern = r'Fourteen Thousand.*?Baht'
            match = re.search(pattern, self.text)
            if match:
                totals['total_in_words'] = match.group(0).strip()

            totals['currency'] = 'THB'
        except Exception as e:
            print(f"⚠ Warning: Error extracting totals - {e}")
        
        return totals

    def build_json_object(self) -> Dict[str, Any]:
        """Build JSON object with extracted data"""
        data = {
            "invoice_number": self.extract_invoice_number(),
            "invoice_date": self.extract_invoice_date(),
            "seller_id": self.extract_seller_id(),
            "seller_username": self.extract_seller_username(),
        }
        data.update(self.extract_totals())
        return data

    def save_json(self, data: Dict[str, Any]) -> Path:
        """Save as JSON array [{ }]"""
        try:
            invoice_date = data.get('invoice_date', 'unknown')
            invoice_num = data.get('invoice_number', 'unknown')
            ref_num = invoice_num.replace('[', '').replace(']', '').split('-')[-1]
            
            filename = f"shopee_invoice_{invoice_date}_{ref_num}.json"
            output_path = self.output_dir / filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump([data], f, indent=2, ensure_ascii=False)
            
            return output_path
        except Exception as e:
            print(f"✗ Error: Failed to save JSON - {e}")
            return None

    def extract(self) -> Tuple[bool, Optional[Path]]:
        """Main extraction workflow"""
        print(f"\n📄 Processing: {self.pdf_path.name}")
        print("─" * 70)
        
        # Extract text from PDF
        if not self.extract_text():
            return False, None
        
        # Build data object
        self.data = self.build_json_object()
        
        # Validate key fields
        if not self.data.get('invoice_number') or not self.data.get('invoice_date'):
            print("✗ Error: Missing key fields (invoice_number or invoice_date)")
            return False, None
        
        # Save as JSON
        output_path = self.save_json(self.data)
        if not output_path:
            return False, None
        
        return True, output_path

    def print_result(self, success: bool, output_path: Optional[Path]) -> None:
        """Print extraction result"""
        if success and output_path:
            print("\n✓ Extraction successful!")
            print(f"✓ Output: {output_path}")
            print("\nExtracted Data:")
            print("─" * 70)
            print(f"  Invoice Number: {self.data.get('invoice_number')}")
            print(f"  Invoice Date:   {self.data.get('invoice_date')}")
            print(f"  Seller ID:      {self.data.get('seller_id')}")
            print(f"  Username:       {self.data.get('seller_username')}")
            print(f"  Subtotal (ex-VAT): ฿{self.data.get('subtotal_before_vat', 0):,.2f}")
            print(f"  VAT (7%):       ฿{self.data.get('vat_amount', 0):,.2f}")
            print(f"  Total (inc-VAT): ฿{self.data.get('total_with_vat', 0):,.2f}")
            print("─" * 70)
        else:
            print("\n✗ Extraction failed!")
            print("─" * 70)


def move_into(src: Path, dest_dir: Path) -> Path:
    """Move src into dest_dir, overwriting any existing file with the same name"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / src.name
    if dest_path.exists():
        dest_path.unlink()
    shutil.move(str(src), str(dest_path))
    return dest_path


def process_download_folder(download_folder: Path) -> Tuple[int, int]:
    """Process every PDF in download_folder, moving the source PDF to
    'inserted' and the extracted JSON to 'processed'"""
    inserted_dir = download_folder / "inserted"
    processed_dir = download_folder / "processed"

    pdf_files = sorted(download_folder.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {download_folder}")
        return 0, 0

    success_count = 0
    failure_count = 0

    for pdf_file in pdf_files:
        extractor = ShopeeInvoiceExtractor(str(pdf_file), str(processed_dir))
        success, output_path = extractor.extract()
        extractor.print_result(success, output_path)

        if success:
            move_into(pdf_file, inserted_dir)
            success_count += 1
        else:
            failure_count += 1

    print(f"\n{'=' * 70}")
    print(f"Done: {success_count} succeeded, {failure_count} failed")
    print(f"{'=' * 70}\n")

    return success_count, failure_count


def main():
    """CLI interface"""
    # No arguments: process every PDF in the .env DOWNLOAD_FOLDER
    if len(sys.argv) < 2:
        download_folder = os.getenv("DOWNLOAD_FOLDER")
        if not download_folder:
            print("✗ Error: DOWNLOAD_FOLDER not set in .env")
            sys.exit(1)

        download_path = Path(download_folder)
        if not download_path.is_dir():
            print(f"✗ Error: DOWNLOAD_FOLDER not found - {download_path}")
            sys.exit(1)

        success_count, failure_count = process_download_folder(download_path)
        sys.exit(0 if failure_count == 0 else 1)

    pdf_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    # Create extractor
    extractor = ShopeeInvoiceExtractor(pdf_file, output_dir)

    # Extract invoice
    success, output_path = extractor.extract()

    # Print result
    extractor.print_result(success, output_path)

    # Exit with status code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
