import json

# 569'luk genel link listesi
with open("links.txt", "r", encoding="utf-8") as f:
    site_linkleri = [x.strip() for x in f if x.strip()]

# 519'luk çekilen hocalar
with open("tum_hocalar.json", "r", encoding="utf-8") as f:
    hocalar = json.load(f)

bizde_olan_linkler = set()

for hoca in hocalar:
    link = hoca.get("profil_linki") or hoca.get("url")
    if link:
        bizde_olan_linkler.add(link.strip())

eksikler = []

yasak_kelime = [
    "akademisyenler",
    "admin",
    "laboratuvarlar",
    "Projects",
    "Event",
    "tez-yazim-kilavuzu",
    "arastirma-birimleri",
    "test"
]

for link in site_linkleri:
    if link not in bizde_olan_linkler:
        if not any(y in link for y in yasak_kelime):
            eksikler.append(link)

print("Eksik link sayısı:", len(eksikler))
print()

for e in eksikler:
    print(e)