"""Génère fr/index.html (version française sur sa propre URL) à partir de index.html (anglais).
À relancer après CHAQUE modification de index.html : python build_fr.py
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()

FR_TITLE = "AZURA Models — Agence de mannequins IA, Côte d'Azur"
FR_DESC = "AZURA Models est une agence de mannequins IA sur la Côte d'Azur. Photos et vidéos courtes de vos produits, portés par nos mannequins virtuelles dans des décors de rêve — livrées en quelques jours, sans shooting."
FR_OG_DESC = "Vos produits, portés par nos mannequins virtuelles, dans des décors de rêve. Livrés en quelques jours."

t = src
# 1. langue et métadonnées
t = t.replace('<html lang="en">', '<html lang="fr">', 1)
t = re.sub(r"<title>.*?</title>", f"<title>{FR_TITLE}</title>", t, count=1)
t = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{FR_DESC}">', t, count=1)
t = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="AZURA Models — Agence de mannequins IA">', t, count=1)
t = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{FR_OG_DESC}">', t, count=1)
t = re.sub(r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="AZURA Models — Agence de mannequins IA">', t, count=1)
t = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{FR_OG_DESC}">', t, count=1)
t = t.replace('<meta property="og:url" content="https://azura-models.com/">', '<meta property="og:url" content="https://azura-models.com/fr/">\n<meta property="og:locale" content="fr_FR">\n<meta property="og:locale:alternate" content="en_GB">')
t = t.replace('<link rel="canonical" href="https://azura-models.com/">', '<link rel="canonical" href="https://azura-models.com/fr/">')
# JSON-LD en français
t = t.replace('"description":"AI model agency on the French Riviera: photos and short videos of your products, worn by virtual models, delivered in days without a photoshoot."', '"description":"Agence de mannequins IA sur la Côte d\'Azur : photos et vidéos courtes de vos produits, portés par des mannequins virtuelles, livrées en quelques jours sans shooting."')
t = t.replace('"url":"https://azura-models.com/",', '"url":"https://azura-models.com/fr/",', 1)
# 2. chemins relatifs (la page vit dans /fr/)
for attr in ("src", "href"):
    t = re.sub(rf'{attr}="(img/|video/|favicon\.ico|mentions-legales\.html)', rf'{attr}="../\1', t)
t = t.replace('src="img/${i}.webp"', 'src="../img/${i}.webp"')
t = re.sub(r"""(['"])(video/|img/)""", r"../", t)  # chemins dans le JavaScript (books, vidéos)
# 3. bouton de langue → lien vers la version anglaise
t = t.replace('<a class="lang" id="lang" href="/fr/" hreflang="fr" lang="fr" aria-label="Version française">FR</a>', '<a class="lang" id="lang" href="/" hreflang="en" lang="en" aria-label="English version">EN</a>')
# 4. script de langue : figer le français, plus de détection automatique
t = t.replace("document.documentElement.lang='en';", "document.documentElement.lang='fr';")
assert "document.documentElement.lang='fr';" in t, "bloc langue introuvable"

os.makedirs(os.path.join(HERE, "fr"), exist_ok=True)
open(os.path.join(HERE, "fr", "index.html"), "w", encoding="utf-8").write(t)
print("fr/index.html généré")
