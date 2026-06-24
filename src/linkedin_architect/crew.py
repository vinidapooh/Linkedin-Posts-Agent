import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class LinkedinArchitect():
    """LinkedinArchitect crew"""

    def __init__(self) -> None:
        # Detect if running in Streamlit Cloud production environment
        if os.environ.get("STREAMLIT_RUNTIME_ENV") or os.environ.get("GROQ_API_KEY"):
            # Production environment: High-speed cloud model via Groq API
            self.llm = LLM(
                model="groq/llama3-70b-8192",
                temperature=0.7,
                api_key=os.environ.get("GROQ_API_KEY")
            )
        else:
            # Local development environment: MacBook Pro local Ollama instance
            self.llm = LLM(
                model="ollama/gemma4:latest",
                base_url="http://localhost:11434"
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
        )