import os
import subprocess
import glob
import re
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# 1. CONFIGURATION DU MOTEUR LOCAL (RTX 3090)
gpu_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.0
)

# 2. OUTIL DE PILOTAGE DYNAMIQUE
@tool("executer_script_ae_dynamique")
def executer_script_ae_dynamique(code_jsx: str) -> str:
    """Nettoie et exécute le code ExtendScript dans After Effects."""
    
    # NETTOYAGE : Suppression des balises Markdown et du blabla
    code_propre = re.sub(r"```[a-zA-Z]*", "", code_jsx).replace("
```", "").strip()
    
    # Isole le code si l'IA a mis du texte autour
    match_code = re.search(r'(var\s+|app\.|if\s*\(|function\s+)', code_propre)
    if match_code:
        code_propre = code_propre[match_code.start():]

    # ZONE SÉCURISÉE : Dossier public (évite le bug d'espace dans le nom d'utilisateur)
    dossier_public = "C:\\Users\\Public"
    chemin_script = os.path.join(dossier_public, "action_studio.jsx")
    
    with open(chemin_script, "w", encoding="utf-8") as f:
        f.write(code_propre)
    
    # Détection automatique de la version After Effects
    pattern = r"C:\Program Files\Adobe\Adobe After Effects *\Support Files\afterfx.exe"
    fichiers_ae = glob.glob(pattern)
    
    if not fichiers_ae:
        return "Erreur : After Effects est introuvable dans Program Files."
    
    try:
        # Exécution via l'argument -r (instance active)
        subprocess.run([fichiers_ae[0], "-r", chemin_script], check=True, timeout=20)
        return "✅ Script exécuté avec succès dans After Effects."
    except Exception as e:
        return f"❌ Erreur lors de l'exécution : {str(e)}"

# 3. CONFIGURATION DE L'AGENT
automate_vfx = Agent(
    role="Ingénieur Pipeline Adobe Senior",
    goal="Exécuter des commandes After Effects en utilisant l'outil dédié.",
    backstory=(
        "Tu es un expert technique. Ton seul but est de traduire les demandes "
        "en code JavaScript (ES3) et de les envoyer à l'outil 'executer_script_ae_dynamique'. "
        "Ne réponds jamais par du texte simple, utilise toujours l'outil."
    ),
    llm=gpu_llm,
    tools=[executer_script_ae_dynamique],
    verbose=True
)

# 4. CONSOLE INTERACTIVE
def lancer_console():
    print("\n" + "="*60)
    print("      STUDIO AI INTERACTIVE - AFTER EFFECTS (RTX 3090)")
    print("      Tape 'exit' pour quitter.")
    print("="*60 + "\n")
    
    while True:
        demande = input("👉 Ton ordre (ex: crée une comp 1080p de 5s) : ")
        if demande.lower() == 'exit':
            break
        if not demande.strip():
            continue
            
        tache = Task(
            description=(
                f"L'utilisateur veut : {demande}. "
                "Traduis cela en code ExtendScript et appelle l'outil 'executer_script_ae_dynamique'. "
                "Assure-toi que le code commence par une vérification de projet : if(!app.project){app.newProject();}"
            ),
            expected_output="Le résultat de l'outil.",
            agent=automate_vfx
        )
        
        equipe = Crew(agents=[automate_vfx], tasks=[tache], process=Process.sequential)
        equipe.kickoff()

if __name__ == "__main__":
    lancer_console()