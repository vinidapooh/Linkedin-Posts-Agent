import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class LinkedinArchitect():
    """LinkedinArchitect crew"""

    def get_llm(self) -> LLM:
        """Dynamically fetch the right LLM depending on the environment"""
        if os.environ.get("STREAMLIT_RUNTIME_ENV") or os.environ.get("GROQ_API_KEY"):
            return LLM(
                model="groq/llama3-70b-8192",
                temperature=0.7,
                api_key=os.environ.get("GROQ_API_KEY")
            )
        else:
            return LLM(
                model="ollama/gemma4:latest",
                base_url="http://localhost:11434"
            )

    @agent
    def linkedin_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_analyst'],
            tools=[SerperDevTool()], 
            verbose=True,
            llm=self.get_llm()
        )

    @agent
    def linkedin_ghostwriter(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_ghostwriter'],
            verbose=True,
            llm=self.get_llm()
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
