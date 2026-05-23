import os
import glob
import subprocess

print("==================================================")
# 1. RECHERCHE AUTOMATIQUE DE TON AFTER EFFECTS
# glob.glob va chercher n'importe quelle année (*) installée dans tes programmes
pattern = r"C:\Program Files\Adobe\Adobe After Effects *\Support Files\afterfx.exe"
versions_trouvees = glob.glob(pattern)

if not versions_trouvees:
    print("❌ ERREUR : Aucun After Effects trouvé dans C:\\Program Files\\Adobe.")
    print("Vérifie que ton logiciel est bien installé sur le disque C:.")
    exit()

chemin_ae = versions_trouvees[0]
print(f"✅ LOGICIEL TROUVÉ : {chemin_ae}")

# 2. CRÉATION DU FICHIER DE TEST (Dans le dossier Public sans espace)
dossier_public = "C:\\Users\\Public"
chemin_jsx = os.path.join(dossier_public, "test_brut.jsx")

code_jsx = """
if(!app.project){app.newProject();}
app.project.items.addComp('TEST_DIRECT_OK', 1920, 1080, 1.0, 5, 25);
"""

with open(chemin_jsx, "w", encoding="utf-8") as f:
    f.write(code_jsx)
print(f"✅ FICHIER JSX CRÉÉ : {chemin_jsx}")

# 3. INJECTION DANS AFTER EFFECTS
print("[...] Injection dans l'interface d'After Effects...")
try:
    # On lance la commande Windows
    subprocess.run([chemin_ae, "-r", chemin_jsx], check=True, timeout=15)
    print("==================================================")
    print("✅ SUCCÈS TOTAL : Regarde ton After Effects, la comp 'TEST_DIRECT_OK' doit être là !")
except Exception as e:
    print(f"❌ ERREUR WINDOWS : {str(e)}")