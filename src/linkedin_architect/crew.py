import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class LinkedinArchitect():
    """LinkedinArchitect crew running completely on OpenAI"""

    def __init__(self) -> None:
        # Heavily ground the primary LLM configuration into OpenAI
        self.llm = LLM(
            model="openai/gpt-4o-mini",
            temperature=0.7,
            api_key=os.environ.get("OPENAI_API_KEY")
        )

    @agent
    def linkedin_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_analyst'],
            tools=[SerperDevTool()], 
            verbose=True,
            llm=self.llm
        )

    @agent
    def linkedin_ghostwriter(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_ghostwriter'],
            verbose=True,
            llm=self.llm
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.linkedin_analyst()
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'],
            agent=self.linkedin_ghostwriter()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            llm=self.llm,
            manager_llm=self.llm
        )
