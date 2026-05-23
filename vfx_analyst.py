from crewai import Agent, Task, Crew, Process, LLM

# 1. Configuration du LLM pour ta RTX 3090
# On force l'usage d'Ollama local
gpu_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.3
)

# 2. Définition de l'Agent
analyste_video = Agent(
    role="Directeur Technique VFX & Coloriste",
    goal="Analyser des concepts de plans pour optimiser le rendu visuel.",
    backstory="Expert post-production habitué aux rendus lourds sur RTX 3090.",
    llm=gpu_llm,
    verbose=True
)

# 3. Définition de la Tâche
analyse_plan = Task(
    description="Propose 3 réglages de Tone Mapping pour un plan cyberpunk sous la pluie.",
    expected_output="Un rapport technique de colorimétrie.",
    agent=analyste_video
)

# 4. Orchestration
equipe_vfx = Crew(
    agents=[analyste_video],
    tasks=[analyse_plan],
    process=Process.sequential
)

# 5. Lancement
if __name__ == "__main__":
    print("\n--- Initialisation de la RTX 3090 ---\n")
    resultat = equipe_vfx.kickoff()
    print("\n--- RÉSULTAT ---\n")
    print(resultat)