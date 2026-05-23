import os
import subprocess
import glob
import re
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# 1. CONFIGURATION DU MOTEUR (RTX 3090)
gpu_llm = LLM(
    model='ollama/llama3.1',
    base_url='http://localhost:11434',
    temperature=0.0
)

# 2. OUTIL DE PILOTAGE "FORTERESSE"
@tool('executer_script_ae_dynamique')
def executer_script_ae_dynamique(code_jsx: str) -> str:
    """Nettoie, valide et injecte le code dans After Effects."""
    
    # Nettoyage sécurisé sans split complexe
    code = code_jsx.replace('```javascript', '').replace('```jsx', '')
    code = code.replace('```', '').strip()
    code = code.replace('console.log', '$.writeln')

    # --- AUTO-CORRECTION DES PARAMÈTRES ADOBE ---
    # Répare l'erreur de hauteur (paramètre 3) si l'IA met 1
    def force_min_height(m):
        prefix, w, h = m.group(1), m.group(2), m.group(3)
        if int(h) < 4: h = "1080"
        return f"{prefix}{w}, {h}"

    code = re.sub(r'(\.addComp\s*\([^,]+,\s*)(\d+),\s*(\d+)', force_min_height, code)

    # Chemin Public (contourne l'espace dans le nom d'utilisateur)
    path_jsx = os.path.join('C:\\Users\\Public', 'action_studio.jsx')
    
    with open(path_jsx, 'w', encoding='utf-8') as f:
        f.write(code)
    
    # Scanner After Effects
    pat = r'C:\Program Files\Adobe\Adobe After Effects *\Support Files\afterfx.exe'
    exe_list = glob.glob(pat)
    
    if not exe_list:
        return "Erreur : After Effects introuvable."
    
    try:
        subprocess.run([exe_list[0], '-r', path_jsx], check=True, timeout=20)
        return "✅ Action effectuée."
    except Exception as e:
        return f"❌ Erreur : {str(e)}"

# 3. L'AGENT INTERFACE STUDIO
automate_vfx = Agent(
    role='Expert Automation After Effects',
    goal='Piloter After Effects sans erreurs.',
    backstory=(
        "Tu es un robot. Syntaxe addComp : (nom, largeur, hauteur, 1.0, duree, fps). "
        "La hauteur est le 3eme paramètre. Ne mets jamais 1 en hauteur."
    ),
    llm=gpu_llm,
    tools=[executer_script_ae_dynamique],
    verbose=True
)

# 4. CONSOLE INTERACTIVE
def lancer_console():
    print("\n" + "="*60)
    print("      STUDIO AI - INTERFACE DYNAMIQUE (RTX 3090)")
    print("="*60 + "\n")
    
    while True:
        demande = input("👉 Ton ordre : ")
        if demande.lower() in ['exit', 'quit']: break
        if not demande.strip(): continue
            
        tache = Task(
            description=f"REQUÊTE : {demande}. Traduis en ExtendScript pur.",
            expected_output="Résultat de l'outil.",
            agent=automate_vfx
        )
        
        crew = Crew(agents=[automate_vfx], tasks=[tache], process=Process.sequential)
        crew.kickoff()

if __name__ == '__main__':
    lancer_console()