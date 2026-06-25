import json
import re

with open("tum_hocalar.json", "r", encoding="utf-8") as f:
    hocalar = json.load(f)

def bilgi_getir(soru):
    soru_kucuk = soru.lower()
    kelimeler = soru_kucuk.replace("?", "").split()

    for hoca in hocalar:
        icerik = hoca["icerik"]
        icerik_kucuk = icerik.lower()

        eslesen = sum(1 for k in kelimeler if k in icerik_kucuk)

        if eslesen >= 2:
            mailler = re.findall(r'[\w\.-]+@[\w\.-]+', icerik)
            telefonlar = re.findall(r'0\s?\(\d+\)\s?\d+', icerik)

            satirlar = [x.strip() for x in icerik.split("\n") if x.strip()]

            print("\nKİŞİ BULUNDU")
            print("Profil:", hoca.get("profil_linki") or hoca.get("url"))

            if "mail" in soru_kucuk or "gmail" in soru_kucuk or "e posta" in soru_kucuk:
                print("Mail:", mailler[0] if mailler else "Bulunamadı")

            elif "telefon" in soru_kucuk or "numara" in soru_kucuk:
                print("Telefon:", telefonlar[0] if telefonlar else "Bulunamadı")

            elif "bölüm" in soru_kucuk or "bolum" in soru_kucuk:
                for s in satirlar:
                    if "Bölümü" in s or "Anabilim Dalı" in s or "Fakültesi" in s:
                        print("Bölüm:", s)
                        break

            else:
                print("\nÖzet Bilgi:")

                filtreler = [
                    "İZÜ Anasayfa", "Kütüphane", "Giriş Yap",
                    "AkademikKadro", "ArastirmacilarIcin", "Laboratuvar",
                    "EtikKurullar", "Kutuphane", "TTO", "BAP",
                    "AkademikIsbirlik", "FikriMulkiyet", "UniversiteSanayi",
                    "Girisimcilik", "TezYazim", "Proje", "DevamEdenProje",
                    "TamamlananProje", "BaslananProje", "Oduller",
                    "AkademikFaaliyetler", "Etkinlikler", "Ulusal Etkinlikler",
                    "Uluslararası Etkinlikler", "Dergiler", "Yayınlarımız",
                    "Atölyeler", "ArastirmaCiktilari", "Makaleler", "Tezler",
                    "Yayin2020", "Akademisyenler", "MENU", "Biyografi",
                    "Öğrenim Bilgisi", "Kitaplar", "Bildiriler", "Projeler",
                    "Dersler", "Yönetilen Tezler", "Ödüller", "Üyelikler",
                    "İdari Görevler", "Üniversite Dışı Deneyim",
                    "Detaylı Özgeçmiş için Tıklayınız.",
                    "ZaimUniversitesi", "ZaimAnasayfa", "Iletisim"
                ]

                temiz_satirlar = []

                for s in satirlar:
                    if s in filtreler:
                        continue
                    if len(s) < 2:
                        continue
                    temiz_satirlar.append(s)

                for s in temiz_satirlar[:12]:
                    print(s)

            return

    print("Sonuç bulunamadı.")

while True:
    soru = input("\nSoru sor veya çıkmak için q yaz: ")

    if soru.lower() == "q":
        print("Çıkılıyor...")
        break

    bilgi_getir(soru)