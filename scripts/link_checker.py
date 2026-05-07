import re
import requests
import sys
from concurrent.futures import ThreadPoolExecutor

def check_link(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return url, response.status_code
    except Exception as e:
        return url, str(e)

def find_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return re.findall(r'\[.*?\]\((https?://.*?)\)', content)

def main():
    target_file = 'README.md'
    links = find_links(target_file)
    print(f"Found {len(links)} links in {target_file}. Checking...")

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_link, links))

    broken_links = [res for res in results if not isinstance(res[1], int) or res[1] >= 400]

    if broken_links:
        print("\n❌ Broken Links Found:")
        for url, status in broken_links:
            print(f" - {url} (Status: {status})")
        sys.exit(1)
    else:
        print("\n✅ All links are working perfectly!")
        sys.exit(0)

if __name__ == "__main__":
    main()
