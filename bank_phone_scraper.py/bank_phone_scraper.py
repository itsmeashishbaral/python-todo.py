import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

banks = {
    "Agriculture Development Bank": "https://adbl.gov.np/",
    "Citizens Bank": "https://www.ctznbank.com/",
    "Everest Bank": "https://everestbankltd.com/",
    "Global IME Bank": "https://www.globalimebank.com/",
    "Himalayan Bank": "https://www.himalayanbank.com/",
    "Kumari Bank": "https://www.kumaribank.com/",
    "Laxmi Sunrise Bank": "https://www.laxmisunrise.com/",
    "Machhapuchhre Bank": "https://www.machbank.com/",
    "Nabil Bank": "https://www.nabilbank.com/",
    "Nepal Bank": "https://nepalbank.com.np/",
    "Nepal Investment Mega Bank": "https://www.nimb.com.np/",
    "Nepal SBI Bank": "https://www.nepalsbi.com.np/",
    "NIC Asia Bank": "https://www.nicasiabank.com/",
    "NMB Bank": "https://www.nmb.com.np/",
    "Prabhu Bank": "https://www.prabhubank.com/",
    "Prime Commercial Bank": "https://www.primebank.com.np/",
    "Rastriya Banijya Bank": "https://www.rbb.com.np/",
    "Sanima Bank": "https://www.sanimabank.com/",
    "Siddhartha Bank": "https://www.siddharthabank.com/",
    "Standard Chartered Bank Nepal": "https://www.sc.com/np/"
}

phone_pattern = re.compile(r"(?:\+977[-\s]?)?(?:\d{1,3}[-\s]?\d{5,8})")

data = []
for name, url in banks.items():
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(separator=" ")
        phones = phone_pattern.findall(text)
        unique = []
        for p in phones:
            clean = p.strip()
            if clean not in unique:
                unique.append(clean)
        data.append({
            "Bank": name,
            "Website": url,
            "Phones": ", ".join(unique[:3]) or "Not found"
        })
        print(f"{name}: {unique[:3]}")
    except Exception as e:
        print(f"Error {name}: {e}")
        data.append({"Bank": name, "Website": url, "Phones": "Error"})

df = pd.DataFrame(data)
df.to_csv("nepal_bank_phones.csv", index=False)
print("Saved to nepal_bank_phones.csv")
