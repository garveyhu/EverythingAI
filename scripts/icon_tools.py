import json
import base64
import sys
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

import ssl

# Domestic Favicon API
API_URL = "https://api.iowen.cn/favicon"

def get_base64_icon(url):
    """
    Fetch favicon from domestic API and convert to base64 data URI.
    Returns None if failed.
    """
    if not url:
        return None
    
    try:
        # Extract domain
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc or parsed.path.split('/')[0]
        if not domain:
            return None
            
        icon_url = f"{API_URL}/{domain}.png"
        
        # request
        req = urllib.request.Request(
            icon_url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        # Ignore SSL errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            data = response.read()
            if not data:
                return None
                
            # Convert to base64
            b64_str = base64.b64encode(data).decode('utf-8')
            mime_type = "image/png" # Google returns png
            return f"data:{mime_type};base64,{b64_str}"
            
    except Exception as e:
        print(f"Error fetching icon for {url}: {e}")
        return None

def process_all_tools(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"File not found: {path}")
        return

    print(f"Processing {path}...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            tools = json.load(f)
        
        count = 0
        total = len(tools)
        
        for i, tool in enumerate(tools):
            title = tool.get('title', 'Unknown')
            url = tool.get('url', '')
            
            # Skip if already has data URI icon (starts with data:)
            # User wants to convert ALL, but maybe we should respect existing generic ones?
            # User said: "support converting ALL links... automatically fill into icon"
            # I will overwrite if it's empty or a http link.
            # If it's already a data URI, I'll skip to save time, unless forced (not implemented).
            
            current_icon = tool.get('icon', '')
            if current_icon and current_icon.startswith('data:'):
                print(f"[{i+1}/{total}] Skipping {title} (Already Base64)")
                continue

            print(f"[{i+1}/{total}] Fetching icon for {title} ({url})...")
            b64 = get_base64_icon(url)
            
            if b64:
                tool['icon'] = b64
                count += 1
                print("  -> Success")
            else:
                print("  -> Failed")

        # Save back
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(tools, f, indent=2, ensure_ascii=False)
            
        print(f"\nDone! Updated {count} icons.")
        
    except Exception as e:
        print(f"Error processing file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Fetch and convert tool icons to Base64")
    parser.add_argument('--test', help="Test a single URL and print Base64 icon")
    parser.add_argument('--all', action='store_true', help=f"Process all tools in scripts/data/tools.json")
    parser.add_argument('--file', default="scripts/data/tools.json", help="Path to tools.json")
    
    args = parser.parse_args()
    
    if args.test:
        print(f"Testing URL: {args.test}")
        icon = get_base64_icon(args.test)
        if icon:
            print("\nBase64 Icon:\n")
            print(icon[:100] + "..." + icon[-20:]) # Truncate for display
            print(f"\n(Length: {len(icon)} chars)")
        else:
            print("Failed to fetch icon.")
            
    elif args.all:
        process_all_tools(args.file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
