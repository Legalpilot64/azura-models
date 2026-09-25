"""PUBLICATION DU SITE — à utiliser pour TOUTE mise en ligne.
Fait dans l'ordre : version de cache (images/vidéos) → génération de fr/index.html → contrôle du JavaScript EN + FR → commit → push.
Usage : python publier.py "message du commit"
"""
import sys, re, subprocess, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
msg = sys.argv[1] if len(sys.argv) > 1 else "Mise à jour du site"

# 1. version de cache : chaque publication change ?v=… sur les images des books et les vidéos
v = datetime.datetime.now().strftime("%Y%m%d%H%M")
t = open("index.html", encoding="utf-8").read()
t2 = re.sub(r'const ASSET_V="[^"]*";', f'const ASSET_V="{v}";', t)
if t2 == t:
    raise SystemExit("ASSET_V introuvable dans index.html")
open("index.html", "w", encoding="utf-8").write(t2)

# 2. page française
subprocess.run([sys.executable, "build_fr.py"], check=True)

# 3. contrôle JavaScript
for f in ["index.html", "fr/index.html"]:
    s = re.findall(r"<script>(.*?)</script>", open(f, encoding="utf-8").read(), flags=re.S)[0]
    open("_c.js", "w", encoding="utf-8").write(s)
    r = subprocess.run(["node", "--check", "_c.js"], capture_output=True, text=True); os.remove("_c.js")
    if r.returncode != 0:
        raise SystemExit(f"ERREUR JavaScript dans {f} :\n{r.stderr[:800]}")
    print(f, "JS OK")

# 4. vérification : les deux pages listent les mêmes images de book
imgs_en = re.findall(r'imgs:\[[^\]]*\]', open("index.html", encoding="utf-8").read())
imgs_fr = re.findall(r'imgs:\[[^\]]*\]', open("fr/index.html", encoding="utf-8").read())
if imgs_en != imgs_fr:
    raise SystemExit("Les books EN et FR diffèrent : ne pas publier")
print("Books EN = FR : OK")

# 5. commit + push
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-q", "-m", msg], check=True)
subprocess.run(["git", "push", "-q", "origin", "main"], check=True)
print("Publié (.com et /fr/) — version de cache", v)
