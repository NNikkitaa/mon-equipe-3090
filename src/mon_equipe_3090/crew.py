from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os

@CrewBase
class MonEquipe3090():
    """Système Crew pour le portfolio de Hensen"""

    # On définit le modèle Qwen 3.6 ici pour qu'il soit partagé par tous les agents
    # Le timeout est mis à 300 secondes car les gros modèles mettent du temps à charger en VRAM
    qwen_llm = LLM(
        model=os.getenv("OPENAI_MODEL_NAME", "ollama/qwen3.6:27b"),
        base_url=os.getenv("OPENAI_API_BASE"), # Doit finir par /v1 sur la plateforme
        api_key="ollama",
        timeout=300,
        temperature=0.3
    )

    @agent
    def expert_technique(self) -> Agent:
        return Agent(
            config=self.agents_config['expert_technique'],
            llm=self.qwen_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def designer_motion(self) -> Agent:
        return Agent(
            config=self.agents_config['designer_motion'],
            llm=self.qwen_llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def recherche_task(self) -> Task:
        return Task(
            config=self.tasks_config['recherche_task'],
        )

    @task
    def developpement_task(self) -> Task:
        return Task(
            config=self.tasks_config['developpement_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Crée l'équipe de production"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )