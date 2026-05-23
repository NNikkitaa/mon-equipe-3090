from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os

@CrewBase
class MonEquipe3090():
    # Ton LLM personnalisé
    qwen_llm = LLM(
        model=os.getenv("OPENAI_MODEL_NAME", "ollama/qwen3.6:27b"),
        base_url=os.getenv("OPENAI_API_BASE"),
        api_key="ollama",
        timeout=300
    )

    @agent
    def expert_technique(self) -> Agent:
        return Agent(
            config=self.agents_config['expert_technique'], # <--- Doit être dans agents.yaml
            llm=self.qwen_llm
        )

    @agent
    def designer_motion(self) -> Agent:
        return Agent(
            config=self.agents_config['designer_motion'], # <--- Doit être dans agents.yaml
            llm=self.qwen_llm
        )

    @task
    def recherche_task(self) -> Task:
        return Task(
            config=self.tasks_config['recherche_task'] # <--- Doit être dans tasks.yaml
        )

    @task
    def developpement_task(self) -> Task:
        return Task(
            config=self.tasks_config['developpement_task'] # <--- Doit être dans tasks.yaml
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )