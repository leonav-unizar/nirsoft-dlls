import requests
import subprocess
from bs4 import BeautifulSoup
import string
import html
import json

def download_report(url : str):
    # For some reason, requests package sometimes fails to retrieve some data
    tmp_file = "tmp.html"
    subprocess.run(["wget", "-O", tmp_file, url], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    with open(tmp_file, encoding="cp1252") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    subprocess.run(["rm", tmp_file])

    return soup

letters = list(string.ascii_lowercase)
base_url = "https://xpdll.nirsoft.net/"
#  XP: "https://xpdll.nirsoft.net/"
#  W7: "https://www.win7dll.info/"
#  W8: "https://www.nirsoft.net/dll_information/windows8/"
# W10: "https://windows10dll.nirsoft.net/"

all_exports = {}
for letter in letters:
    req = requests.get(f"{base_url}{letter}.html")
    dll_page_list = BeautifulSoup(html.unescape(req.text), "html.parser")

    dll_list = dll_page_list.select('table')
    if len(dll_list) < 5:
        print(f"No DLLs available with the letter {letter}")
        continue

    dll_list = dll_list[4].find_all('tr')
    dll_list.pop(0)
    for dll in dll_list:
        dll_link = dll.find('a', href=True)

        print(f" [i] {base_url}{dll_link["href"]}")
        soup2 = download_report(f"{base_url}{dll_link["href"]}")

        if "This dll doesn't export any function" in soup2.text:
            all_exports[dll_link.text] = "No exports"

        else:
            exported_header = soup2.find('h4', string='Exported Functions List')
            if not exported_header:
                print("[!] Exported functions not available")
                continue

            exported_table = exported_header.find_next('table')
            raw_text = exported_table.get_text()
            functions = [
                line.strip()
                for line in raw_text.splitlines()
                if line.strip()
            ]

            functions = list(set(functions))
            all_exports[dll_link.text] = list(set(functions))

with open("exported-functions.json", "w", encoding="utf-8") as f:
    json.dump(all_exports, f, indent=2)
