#!/usr/bin/env python3
"""Convert PDF presentation pages to PNG images for interactive slides."""

import argparse
import pathlib
import sys
from typing import Optional

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF is required. Install it with: pip install pymupdf")
    sys.exit(1)


ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT_DIR / "blog"
DEFAULT_OUTPUT_DIR = BLOG_DIR / "assets/images/slides"
DEFAULT_DPI = 300


def pdf_to_images(
    pdf_path: pathlib.Path,
    output_dir: pathlib.Path,
    dpi: int = DEFAULT_DPI,
    prefix: Optional[str] = None,
) -> None:
    """Convert PDF pages to JPG images.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save JPG images
        dpi: Resolution in DPI (default: 300)
        prefix: Optional prefix for output filenames (default: PDF basename)
    """
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == ".pdf":
        print(f"Error: File is not a PDF: {pdf_path}")
        sys.exit(1)
    
    # Determine prefix from PDF filename if not provided
    if prefix is None:
        prefix = pdf_path.stem
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting PDF: {pdf_path.name}")
    print(f"Output directory: {output_dir}")
    print(f"DPI: {dpi}")
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        page_count = len(doc)
        print(f"Found {page_count} pages")
        
        # Target max width in pixels
        max_width = 1200
        
        # Convert each page to image
        for page_num in range(page_count):
            page = doc[page_num]
            
            # Calculate zoom to get max 1200px width
            # Get page dimensions in points (72 points = 1 inch)
            page_rect = page.rect
            page_width_points = page_rect.width
            
            # Calculate zoom to achieve target width
            # At 72 DPI (zoom=1.0), width in pixels = width in points
            # So zoom = target_width / page_width_points
            zoom = max_width / page_width_points
            
            # Create transformation matrix
            mat = fitz.Matrix(zoom, zoom)
            
            # Render page to pixmap with RGB color space to avoid darkening
            # Use alpha=False for better compatibility
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # Convert to RGB if not already (handles CMYK and other color spaces)
            if pix.colorspace.name != fitz.csRGB.name:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            
            # Save as PNG (lossless)
            if prefix:
                output_filename = f"{prefix}-{page_num + 1:02d}.png"
            else:
                output_filename = f"slide-{page_num + 1:02d}.png"
            output_path = output_dir / output_filename
            
            # Save as PNG (lossless format)
            pix.save(output_path, output="png")
            print(f"Saved: {output_filename}")
        
        doc.close()
        
        print(f"\nSuccessfully converted {page_count} pages to PNG images")
        
    except Exception as e:
        print(f"Error converting PDF: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert PDF presentation pages to PNG images for interactive slides"
    )
    parser.add_argument(
        "pdf",
        type=pathlib.Path,
        help="Path to the PDF file to convert",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for PNG images (default: {DEFAULT_OUTPUT_DIR.relative_to(ROOT_DIR)})",
    )
    parser.add_argument(
        "-d",
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help=f"Resolution in DPI (default: {DEFAULT_DPI}, good for web display)",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        default=None,
        help="Prefix for output filenames (default: PDF filename without extension)",
    )
    
    args = parser.parse_args()
    
    # Resolve relative paths relative to script location
    pdf_path = args.pdf
    if not pdf_path.is_absolute():
        pdf_path = (pathlib.Path.cwd() / pdf_path).resolve()
    
    output_dir = args.output
    if not output_dir.is_absolute():
        output_dir = (pathlib.Path.cwd() / output_dir).resolve()
    
    pdf_to_images(
        pdf_path=pdf_path,
        output_dir=output_dir,
        dpi=args.dpi,
        prefix=args.prefix,
    )


if __name__ == "__main__":
    main()

