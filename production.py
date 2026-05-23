import os
import subprocess
import glob
import re
import time
import json
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# --- 1. CONFIGURATION DU MOTEUR (RTX 3090 & QWEN 3.6) ---
# On utilise les variables d'environnement pour la flexibilité (Local vs Plateforme)
gpu_llm = LLM(
    model=os.getenv("OPENAI_MODEL_NAME", "ollama/qwen3.6:27b"),
    base_url=os.getenv("OPENAI_API_BASE", "http://localhost:11434/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "ollama"),
    timeout=300,
    temperature=0.1 # Précision maximale pour le code
)

# --- 2. OUTIL : SCANNER DE COMPOSITION ACTIVE ---
@tool('scanner_contexte_ae')
def scanner_contexte_ae() -> str:
    """Scanne uniquement la composition active pour économiser la mémoire et le contexte."""
    
    jsx_scanner = """
    (function() {
        var activeItem = app.project.activeItem;
        var report = { status: "no_active_comp", data: {} };

        if (activeItem && activeItem instanceof CompItem) {
            report.status = "active_comp_found";
            report.data = {
                name: activeItem.name,
                width: activeItem.width,
                height: activeItem.height,
                duration: activeItem.duration,
                layers: []
            };

            for (var j = 1; j <= activeItem.numLayers; j++) {
                var l = activeItem.layer(j);
                report.data.layers.push({
                    index: l.index,
                    name: l.name,
                    type: (l instanceof TextLayer) ? "Texte" : (l instanceof ShapeLayer) ? "Forme" : "Solide/Autre",
                    locked: l.locked,
                    visible: l.enabled
                });
            }
        } else {
            // Si rien n'est actif, on liste juste les noms des compos du projet
            report.status = "project_summary";
            var comps = [];
            for (var i = 1; i <= app.project.numItems; i++) {
                if (app.project.item(i) instanceof CompItem) {
                    comps.push(app.project.item(i).name);
                }
            }
            report.data = { project_comps: comps };
        }

        var f = new File("C:/Users/Public/ae_context.json");
        f.open("w");
        f.write(JSON.stringify(report));
        f.close();
        return "SCAN_DONE";
    })();
    """

    path_jsx = os.path.join('C:\\Users\\Public', 'scanner_context.jsx')
    path_json = os.path.join('C:\\Users\\Public', 'ae_context.json')

    try:
        with open(path_jsx, 'w', encoding='utf-8') as f:
            f.write(jsx_scanner)
        
        ae_exe = glob.glob(r'C:\Program Files\Adobe\Adobe After Effects *\Support Files\afterfx.exe')[-1]
        subprocess.run([ae_exe, '-r', path_jsx], check=True, timeout=25)
        
        time.sleep(1)
        if os.path.exists(path_json):
            with open(path_json, 'r', encoding='utf-8') as f:
                return f.read()
        return "Erreur : Fichier de scan non généré."
    except Exception as e:
        return f"Erreur lors du scan : {str(e)}"

# --- 3. OUTIL : PILOTAGE AE AVEC AUTO-CORRECTION ---
@tool('pilotage_ae_intelligent')
def pilotage_ae_intelligent(code_jsx: str) -> str:
    """Exécute du code ExtendScript avec capture d'erreurs en temps réel."""
    
    # Nettoyage Markdown
    code = re.sub(r'```(?:javascript|jsx)?', '', code_jsx)
    code = code.replace('```', '').strip()
    
    # Encapsulation pour retour d'erreur
    code_final = f"""
    (function() {{
        try {{
            {code}
            var res = "SUCCESS";
        }} catch(e) {{
            var res = "ERREUR_AE: " + e.message + " (Ligne: " + e.line + ")";
        }}
        var f = new File("C:/Users/Public/ae_result.log");
        f.open("w");
        f.write(res);
        f.close();
    }})();
    """

    path_jsx = os.path.join('C:\\Users\\Public', 'action_studio.jsx')
    path_log = os.path.join('C:\\Users\\Public', 'ae_result.log')

    try:
        with open(path_jsx, 'w', encoding='utf-8') as f:
            f.write(code_final)
        
        ae_exe = glob.glob(r'C:\Program Files\Adobe\Adobe After Effects *\Support Files\afterfx.exe')[-1]
        subprocess.run([ae_exe, '-r', path_jsx], check=True, timeout=30)
        
        time.sleep(1)
        if os.path.exists(path_log):
            with open(path_log, 'r', encoding='utf-8') as f:
                res = f.read()
            if "ERREUR_AE" in res:
                return f"Échec. After Effects a renvoyé : {res}. Analyse et corrige."
            return "✅ Succès."
        return "⚠️ Pas de log de retour."
    except Exception as e:
        return f"Erreur système : {str(e)}"

# --- 4. L'AGENT ET LA TASK ---
automate_vfx = Agent(
    role='Directeur Technique After Effects',
    goal='Analyser la compo active et exécuter des modifications sans erreurs.',
    backstory=(
        "Tu es un expert qui 'voit' à l'intérieur d'After Effects. "
        "Avant toute action, utilise 'scanner_contexte_ae' pour comprendre où tu es. "
        "Si une erreur survient, déchiffre le message pour te corriger."
    ),
    llm=gpu_llm,
    tools=[scanner_contexte_ae, pilotage_ae_intelligent],
    verbose=True,
    max_iter=5
)

def lancer_studio():
    print("\n" + "═"*60)
    print("        🚀 STUDIO AI - MODE CONTEXTUEL (RTX 3090)")
    print("═"*60 + "\n")
    
    while True:
        ordre = input("👉 Ordre After Effects : ")
        if ordre.lower() in ['exit', 'quit']: break
            
        tache = Task(
            description=(
                f"Ordre : {ordre}. \n"
                "1. Scanne la compo pour voir les calques. \n"
                "2. Si la compo cible n'est pas active, demande à l'utilisateur ou cherche-la. \n"
                "3. Exécute le code JSX via l'outil de pilotage."
            ),
            expected_output="Résultat de l'opération après analyse du contexte.",
            agent=automate_vfx
        )
        
        crew = Crew(agents=[automate_vfx], tasks=[tache], process=Process.sequential)
        crew.kickoff()

if __name__ == '__main__':
    lancer_studio()