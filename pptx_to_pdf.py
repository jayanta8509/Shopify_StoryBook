"""
Universal PPTX to PDF Converter
Works on both Linux and Windows - automatically detects platform
"""

import subprocess
import os
import platform
from pathlib import Path


def pptx_to_pdf(pptx_path, output_path=None):
    """
    Convert PPTX to PDF. Automatically detects platform and uses appropriate method.
    
    Args:
        pptx_path (str): Path to the input PPTX file
        output_path (str): Path for output PDF (optional, default: same location as input)
    
    Returns:
        str: Path to the generated PDF file
    
    Raises:
        FileNotFoundError: If input file doesn't exist
        Exception: If conversion fails
    """
    pptx_path = Path(pptx_path).resolve()
    
    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX file not found: {pptx_path}")
    
    # Determine output path
    if output_path is None:
        output_path = pptx_path.with_suffix('.pdf')
    else:
        output_path = Path(output_path).resolve()
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Detect platform and convert
    system = platform.system()
    
    if system == "Windows":
        return _convert_windows(pptx_path, output_path)
    elif system == "Linux":
        return _convert_linux(pptx_path, output_path)
    else:
        # For macOS or other systems, try LibreOffice
        return _convert_libreoffice(pptx_path, output_path)


def _convert_windows(pptx_path, output_path):
    """Convert using Windows COM interface (PowerPoint) with LibreOffice fallback."""
    
    # Try PowerPoint COM first
    try:
        import comtypes.client
        
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 0  # Run in background
        
        try:
            presentation = powerpoint.Presentations.Open(str(pptx_path), WithWindow=False)
            presentation.SaveAs(str(output_path), 32)  # 32 = PDF format
            presentation.Close()
            
            print(f"✓ Converted using PowerPoint: {output_path}")
            return str(output_path)
            
        finally:
            powerpoint.Quit()
            
    except (ImportError, Exception) as e:
        print(f"PowerPoint COM failed ({e}), trying LibreOffice...")
        return _convert_libreoffice(pptx_path, output_path)


def _convert_linux(pptx_path, output_path):
    """Convert using LibreOffice on Linux."""
    return _convert_libreoffice(pptx_path, output_path)


def _convert_libreoffice(pptx_path, output_path):
    """Convert using LibreOffice command line (cross-platform)."""
    
    output_dir = output_path.parent
    
    # LibreOffice conversion command
    cmd = [
        'libreoffice',
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', str(output_dir),
        str(pptx_path)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        # LibreOffice creates PDF with same name as input
        default_pdf = output_dir / f"{pptx_path.stem}.pdf"
        
        # Rename if output path is different
        if default_pdf != output_path and default_pdf.exists():
            default_pdf.rename(output_path)
        
        if output_path.exists():
            print(f"✓ Converted using LibreOffice: {output_path}")
            return str(output_path)
        else:
            raise Exception("PDF was not created")
            
    except subprocess.TimeoutExpired:
        raise Exception("Conversion timeout (5 minutes exceeded)")
    except subprocess.CalledProcessError as e:
        raise Exception(f"LibreOffice conversion failed: {e.stderr}")
    except FileNotFoundError:
        raise Exception(
            "LibreOffice not found. Please install:\n"
            "  Linux: sudo apt-get install libreoffice\n"
            "  Windows: Download from https://www.libreoffice.org/"
        )


# Example usage
if __name__ == "__main__":
    import sys
    
    # Single file conversion
    print("Platform:", platform.system())
    print("-" * 50)
    
    try:
        # Example 1: Convert single file
        pdf_path = pptx_to_pdf("Storybook_Template_1_female.pptx")
        print(f"\nSuccess! PDF saved to: {pdf_path}")
        
        # Example 2: Convert with custom output path
        # pdf_path = pptx_to_pdf("input.pptx", "output/converted.pdf")
        
        # Example 3: Batch convert all PPTX files in a directory
        # results = batch_convert("./presentations", "./pdfs")
        
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)