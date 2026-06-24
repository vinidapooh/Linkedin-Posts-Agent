from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class LinkedinArchitect(): # Updated from YoutubeArchitect
    """LinkedinArchitect crew"""

    llm = LLM(
        model="ollama/gemma4:latest",
        base_url="http://localhost:11434"
    )

    @agent
    def linkedin_analyst(self) -> Agent: # Renamed for clarity
        return Agent(
            config=self.agents_config['linkedin_analyst'],
            tools=[SerperDevTool()], 
            verbose=True,
            llm=self.llm
        )

    @agent
    def linkedin_ghostwriter(self) -> Agent: # Renamed for clarity
        return Agent(
            config=self.agents_config['linkedin_ghostwriter'],
            verbose=True,
            llm=self.llm
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )