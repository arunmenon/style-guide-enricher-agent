from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileReadTool, FileWriterTool

@CrewBase
class StyleGuideAugmentationCrew:
    """StyleGuideAugmentation crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def style_guide_researcher(self) -> Agent:
        # Uses SerperDevTool to discover best practices externally
        # Optionally could use FileWriterTool to store interim notes if needed
        return Agent(
            config=self.agents_config['style_guide_researcher'],
            tools=[SerperDevTool(), FileWriterTool()],
            verbose=True
        )

    @agent
    def style_guide_enhancer(self) -> Agent:
        # Uses FileReadTool to read the base template and research findings
        # Uses FileWriterTool if it wants to store intermediate versions before final output
        return Agent(
            config=self.agents_config['style_guide_enhancer'],
            tools=[FileReadTool(), FileWriterTool()],
            verbose=True
        )

    @agent
    def style_guide_reviewer(self) -> Agent:
        # Uses FileReadTool to read both updated and base templates for comparison
        return Agent(
            config=self.agents_config['style_guide_reviewer'],
            tools=[FileReadTool()],
            verbose=True
        )

    @task
    def research_fashion_trends_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_fashion_trends_task'],
            output_file='research_findings.md'  # Results from researcher
        )

    @task
    def augment_style_guide_task(self) -> Task:
        return Task(
            config=self.tasks_config['augment_style_guide_task'],
            # The enhancer reads base_style_guide_template.md and research_findings.md (both local files)
            # and produces updated_style_guide.md as final output
            output_file='updated_style_guide.md'
        )

    @task
    def review_style_guide_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_style_guide_task']
            # The reviewer reads updated_style_guide.md and base_style_guide_template.md for compliance checking
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StyleGuideAugmentation crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
