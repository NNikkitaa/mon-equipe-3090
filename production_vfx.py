from crewai import Agent, Task, Crew, Process, LLM

# 1. Configuration du LLM (Optimisé pour ta RTX 3090)
gpu_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.4 # Un peu plus de créativité pour le scénario
)

# 2. Définition des Agents
analyste_vfx = Agent(
    role="Directeur Technique VFX & Coloriste",
    goal="Définir des réglages visuels cyber-grunge précis.",
    backstory="Expert en post-production. Tu dictes les contraintes techniques du rendu.",
    llm=gpu_llm,
    verbose=True
)

scenariste = Agent(
    role="Scénariste de Cinéma Cyber-grunge",
    goal="Écrire une séquence de 15 secondes basée sur les contraintes techniques.",
    backstory="Spécialiste des ambiances sombres et viscérales. Tu transformes la technique en émotion.",
    llm=gpu_llm,
    verbose=True
)

# 3. Définition des Tâches
tache_analyse = Task(
    description="Propose 3 réglages techniques pour un plan de ville néon sous la pluie (look cyber-grunge).",
    expected_output="Un rapport technique de colorimétrie et de texture.",
    agent=analyste_vfx
)

tache_script = Task(
    description=(
        "En utilisant les réglages techniques fournis par l'analyste, écris un script "
        "de 15 secondes pour un plan d'ouverture. Inclus la description de l'action, "
        "les mouvements de caméra et des indications de sound design."
    ),
    expected_output="Un script de tournage court (15s) avec indications visuelles et sonores.",
    agent=scenariste,
    context=[tache_analyse] # C'est ici que la magie opère : le scénariste lit l'analyste.
)

# 4. Orchestration séquentielle
equipe_prod = Crew(
    agents=[analyste_vfx, scenariste],
    tasks=[tache_analyse, tache_script],
    process=Process.sequential # L'ordre est respecté : l'un après l'autre.
)

# 5. Lancement
if __name__ == "__main__":
    print("\n--- Lancement de la chaîne de production locale ---\n")
    resultat = equipe_prod.kickoff()
    print("\n--- SCRIPT DE PRODUCTION FINAL ---\n")
    print(resultat)