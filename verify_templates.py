"""
Template Verification Script
Checks if all required PowerPoint template files exist
"""
import os
from pathlib import Path

def verify_templates():
    """Verify that all required template files exist"""
    
    # Define required templates
    templates = {
        "Story 1 (Male)": "story_book/Storybook_Template_1_male.pptx",
        "Story 1 (Female)": "story_book/Storybook_Template_1_female.pptx",
        "Story 2 (Male)": "story_book/Storybook_Template_2_male.pptx",
        "Story 2 (Female)": "story_book/Storybook_Template_2_female.pptx"
    }
    
    print("=" * 70)
    print("POWERPOINT TEMPLATE VERIFICATION")
    print("=" * 70)
    print()
    
    # Check if story_book folder exists
    if not os.path.exists("story_book"):
        print("❌ ERROR: 'story_book' folder does not exist!")
        print("   Please create it with: mkdir story_book")
        print()
        return False
    else:
        print("✅ 'story_book' folder exists")
        print()
    
    # Check each template
    all_exist = True
    missing_templates = []
    existing_templates = []
    
    print("Checking template files:")
    print("-" * 70)
    
    for name, path in templates.items():
        if os.path.exists(path):
            file_size = os.path.getsize(path) / 1024  # KB
            print(f"✅ {name:20} - {path}")
            print(f"   Size: {file_size:.2f} KB")
            existing_templates.append(name)
        else:
            print(f"❌ {name:20} - {path}")
            print(f"   STATUS: MISSING!")
            missing_templates.append((name, path))
            all_exist = False
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ Found: {len(existing_templates)}/4 templates")
    print(f"❌ Missing: {len(missing_templates)}/4 templates")
    print()
    
    if missing_templates:
        print("Missing templates:")
        for name, path in missing_templates:
            print(f"  - {path}")
        print()
        print("⚠️  Please add the missing template files to continue.")
        print("    Refer to SETUP_TEMPLATES.md for detailed instructions.")
    else:
        print("🎉 All template files are present!")
        print("    You can now use the /generate-pptx API endpoint.")
    
    print()
    return all_exist


def list_existing_pptx_files():
    """List all .pptx files in the current directory"""
    print("=" * 70)
    print("EXISTING .PPTX FILES IN PROJECT")
    print("=" * 70)
    print()
    
    pptx_files = list(Path(".").glob("*.pptx"))
    
    if pptx_files:
        print(f"Found {len(pptx_files)} .pptx file(s) in the root directory:")
        for file in pptx_files:
            file_size = os.path.getsize(file) / 1024  # KB
            print(f"  📄 {file.name} ({file_size:.2f} KB)")
        print()
        print("💡 TIP: You can copy these files to the story_book folder and rename them")
        print("        according to the naming convention.")
    else:
        print("No .pptx files found in the root directory.")
    
    print()


if __name__ == "__main__":
    # List existing PPTX files first
    list_existing_pptx_files()
    
    # Verify templates
    verify_templates()

