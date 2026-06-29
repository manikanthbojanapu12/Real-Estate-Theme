import os
import re
from PIL import Image

# Ensure Pillow has AVIF support registered
try:
    import pillow_avif
except ImportError:
    pass

def convert_avif_to_webp(directory, delete_original=False):
    print(f"Starting AVIF to WebP conversion in: {directory}")
    converted_files = {}
    avif_files = []
    
    # 1. Scan for .avif files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.avif'):
                avif_files.append(os.path.join(root, file))
                
    if not avif_files:
        print("No .avif files found in this directory.")
        return
        
    print(f"Found {len(avif_files)} AVIF file(s) to convert.")
    
    # 2. Convert each file
    for filepath in avif_files:
        try:
            webp_path = os.path.splitext(filepath)[0] + '.webp'
            print(f"Converting: {filepath} -> {webp_path}")
            
            with Image.open(filepath) as img:
                img.save(webp_path, 'WEBP', quality=85)
                
            converted_files[filepath] = webp_path
            
            if delete_original:
                os.remove(filepath)
                print(f"Deleted original: {filepath}")
        except Exception as e:
            print(f"Failed to convert {filepath}: {e}")
            
    # 3. Update references in HTML, CSS, JS files
    if converted_files:
        print("\nUpdating image references in HTML, CSS, and JS files...")
        update_references(directory, converted_files)
        
    print("\nConversion process completed successfully.")

def update_references(directory, converted_map):
    # Prepare filename patterns to replace
    replacements = {}
    for old_path, new_path in converted_map.items():
        old_name = os.path.basename(old_path)
        new_name = os.path.basename(new_path)
        replacements[old_name] = new_name
        
        # Also handle relative path updates if needed
        
    if not replacements:
        return
        
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.html', '.css', '.js')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    modified = False
                    for old_name, new_name in replacements.items():
                        # Use regex to find and replace filename references safely
                        pattern = re.escape(old_name)
                        if re.search(pattern, content, re.IGNORECASE):
                            content = re.sub(pattern, new_name, content, flags=re.IGNORECASE)
                            modified = True
                            print(f"  Updated references to {old_name} in {file}")
                            
                    if modified:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                except Exception as e:
                    print(f"  Error updating file {file}: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert AVIF images to WebP and update code references.")
    parser.add_argument("--dir", default=".", help="Directory to scan (default: current directory)")
    parser.add_argument("--delete", action="store_true", help="Delete original AVIF files after conversion")
    args = parser.parse_args()
    
    target_dir = os.path.abspath(args.dir)
    convert_avif_to_webp(target_dir, delete_original=args.delete)
