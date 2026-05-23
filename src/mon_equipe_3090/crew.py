from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os

@CrewBase
class MonEquipe3090():
    """Système Crew pour le portfolio de Hensen"""

    # Configuration du LLM pour ta 3090
    qwen_llm = LLM(
        model=os.getenv("OPENAI_MODEL_NAME", "ollama/qwen3.6:27b"),
        base_url=os.getenv("OPENAI_API_BASE"),
        api_key="ollama",
        timeout=300
    )

    @agent
    def expert_technique(self) -> Agent:
        return Agent(
            config=self.agents_config['expert_technique'], # Doit correspondre au YAML
            llm=self.qwen_llm,
            verbose=True
        )

    @agent
    def designer_motion(self) -> Agent:
        return Agent(
            config=self.agents_config['designer_motion'], # Doit correspondre au YAML
            llm=self.qwen_llm,
            verbose=True
        )

    @task
    def recherche_task(self) -> Task:
        return Task(
            config=self.tasks_config['recherche_task'] # Doit correspondre au YAML
        )

    @task
    def developpement_task(self) -> Task:
        return Task(
            config=self.tasks_config['developpement_task'] # Doit correspondre au YAML
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )