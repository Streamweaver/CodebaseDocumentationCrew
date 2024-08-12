"""A CrewAI-based tool for generating codebase documentation from a given repository."""
import json
from datetime import datetime
from textwrap import dedent
from typing import Dict, List, Tuple, Union
from crewai import Agent, Task, Crew, Process
from langchain_core.agents import AgentFinish
import streamlit as st
from .tools import DirectoryReadTool, AbsPathFileReadTool

class CodebaseDocumentationCrew:
    def __init__(self, repo_path, llm, file_label="code_documentation"):
        self.repo_path = repo_path
        self.ignore_dirs = ['.git', '.idea', '.vscode', '__pycache__', 'node_modules', 'venv', 'env']
        self.directory_tool = DirectoryReadTool(directory=repo_path, ignore_dirs=self.ignore_dirs)
        self.file_tool = AbsPathFileReadTool(self.repo_path)
        
        self.llm = llm

        # Initialize agent variables
        self.repository_analyzer = None
        self.code_reviewer = None
        self.documentation_writer = None
        self.markdown_formatter = None
        
        # Initialize task variables
        self.analyze_repo_structure = None
        self.review_code_components = None
        self.write_documentation = None
        self.format_documentation = None

        self._output_file_label = file_label

        self.create_agents()
        self.create_tasks()

    def step_callback(
        self,
        agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish],
        agent_name,
        *args,
    ):
        with st.chat_message("AI"):
            # Try to parse the output if it is a JSON string
            if isinstance(agent_output, str):
                try:
                    agent_output = json.loads(agent_output)
                except json.JSONDecodeError:
                    pass

            if isinstance(agent_output, list) and all(
                isinstance(item, tuple) for item in agent_output
            ):

                for action, description in agent_output:
                    # Print attributes based on assumed structure
                    st.write(f"Agent Name: {agent_name}")
                    st.write(f"Tool used: {getattr(action, 'tool', 'Unknown')}")
                    st.write(f"Tool input: {getattr(action, 'tool_input', 'Unknown')}")
                    st.write(f"{getattr(action, 'log', 'Unknown')}")
                    with st.expander("Show observation"):
                        st.markdown(f"Observation\n\n{description}")

            # Check if the output is a dictionary as in the second case
            elif isinstance(agent_output, AgentFinish):
                st.write(f"Agent Name: {agent_name}")
                output = agent_output.return_values
                st.write(f"I finished my task:\n{output['output']}")

            # Handle unexpected formats
            else:
                st.write(type(agent_output))
                st.write(agent_output)

    def create_agents(self):
        # file_tool_instruction = (
        #     "When using the Read File tool, always provide file paths relative to the repository root. "
        #     "For example, use 'src/main.py' instead of '/src/main.py' or './src/main.py'."
        # )
                
        self.repository_analyzer = Agent(
            role='Repository Analyzer',
            goal=dedent(
                """Conduct an exhaustive analysis of the codebase structure, identifying all key 
                components, dependencies, and architectural patterns while providing a detailed 
                map of the project's organization."""
                ),
            backstory=dedent(
                """You are a veteran software architect with decades of experience in dissecting 
                complex codebases across various industries. Your keen eye for design patterns 
                and ability to quickly grasp intricate system interactions have made you the 
                go-to expert for understanding large-scale software projects. You've developed a 
                proprietary method for creating visual and textual representations of code 
                structures that even novice developers can understand. Your analysis forms the 
                foundation upon which all other documentation is built."""
                ),
            tools=[self.directory_tool, self.file_tool],
            verbose=True,
            llm=self.llm
        )

        self.code_reviewer = Agent(
            role='Code Reviewer',
            goal=dedent(
                """Perform a meticulous review of all code components, uncovering and documenting 
                every feature, function, class, and their interactions while assessing code quality, 
                performance implications, and adherence to best practices."""
                ),
            backstory=dedent(
                """As a renowned code review specialist, you've honed your skills through years of 
                contributing to open-source projects and leading development teams at top tech 
                companies. Your extraordinary ability to understand code at both micro and macro 
                levels allows you to provide insights that go beyond mere functionality. You're 
                known for your comprehensive reviews that not only explain what the code does but 
                why it's structured that way, potential optimizations, and how it fits into the larger 
                system architecture. Your analyses have helped countless teams improve their codebases 
                and onboard new developers efficiently"""
                ),
            tools=[self.file_tool],
            verbose=True,
            llm=self.llm,
            step_callback=lambda step: self.step_callback(step, "Code Reviewer")
        )

        self.documentation_writer = Agent(
            role='Documentation Writer',
            goal=dedent(
                """With a unique background in both software engineering and technical writing, you've 
                become the bridge between complex code and human understanding. Your documentation has 
                been praised across the industry for its clarity, completeness, and ability to make even 
                the most intricate systems accessible. You've developed a knack for anticipating questions 
                developers might have and addressing them proactively in your writing. Your work has been 
                used as a benchmark for documentation best practices in numerous tech companies and
                open-source projects."""
                ),
            backstory=dedent(
                """You are a skilled technical writer with a strong background in software development. 
                You can translate complex software functionality and architecture into clear, concise, 
                and well-structured documentation that is easily understood by developers of all skill levels."""
                ),
            verbose=True,
            llm=self.llm,
            step_callback=lambda step: self.step_callback(step, "Documentation Writer")
        )

        # No longer useed.
        self.markdown_formatter = Agent(
            role='Markdown Formatter',
            goal=dedent(
                """Create a visually stunning, highly organized, and easily navigable markdown document that 
                enhances readability and user experience while ensuring all technical content is presented in 
                the most effective manner possible."""
                ),
            backstory=dedent(
                """As a markdown virtuoso, you've elevated technical documentation formatting to an art form. 
                Your background in UX design, combined with your deep understanding of developer needs, allows 
                you to create documents that are not just readable, but a joy to navigate. You've developed 
                custom markdown extensions and styling techniques that have been adopted by major tech companies 
                for their internal and public-facing documentation. Your formatted documents are known for their 
                intuitive structure, making complex information easy to find and understand, even in the largest 
                and most complicated projects."""
                ),
            verbose=True,
            llm=self.llm,
            step_callback=lambda step: self.step_callback(step, "Markdown Formatter")
        )

    def create_tasks(self):
        self.analyze_repo_structure = Task(
            description=dedent(
                f"""Conduct a thorough analysis of the repository structure at {self.repo_path}. Your task is to:
                        1. Map out the complete directory structure, noting the purpose of each folder.
                        2. Identify all key files, including source code, configuration files, and assets.
                        3. Detect any design patterns evident in the file organization.
                        4. Analyze naming conventions used throughout the project.
                        5. Identify any modular or microservice architecture if present.
                        6. Note any deviation from standard project structures for the main programming language(s) 
                           used.
                        7. Highlight any build, test, or deployment scripts.
                        8. Identify documentation files or folders.
                        9. Please refer to all files by their absolute filepath. The following directories should be 
                           excluded from your analysis: {', '.join(self.ignore_dirs)}."""
                ),
            agent=self.repository_analyzer,
            expected_output=dedent(
                """Provide a detailed report on the repository structure that includes:
                        1. A hierarchical representation of the directory structure with descriptions for each significant folder.
                        2. A list of key files with brief descriptions of their purposes.
                        3. An analysis of the overall architectural approach evident from the file organization.
                        4. Insights into the project's adherence to or deviation from standard practices.
                        5. Identification of any missing crucial components or folders.
                        6. Recommendations for improving the repository structure if applicable.
                        7. A summary of the build and deployment setup based on relevant scripts or configuration files found."""
                ),
            callback=self.task_callback
        )

        self.review_code_components = Task(
            description=dedent(
                """Based on the repository analysis, perform a comprehensive review of the main code components. Your task involves:
                        1. Identifying and describing key features and functionalities of the project.
                        2. Analyzing important classes and functions, noting their purposes and interactions.
                        3. Recognizing and explaining design patterns and architectural decisions.
                        4. Evaluating the code quality, including readability, modularity, and adherence to best practices.
                        5. Assessing error handling and logging mechanisms.
                        6. Identifying any performance optimizations or scalability considerations.
                        7. Noting the use of external libraries, APIs, or services and their integration.
                        8. Analyzing any database schemas or data models used.
                        9. Reviewing test coverage and testing strategies employed.
                        10. Identifying potential areas for improvement or refactoring."""
                ),
            agent=self.code_reviewer,
            expected_output=dedent(
                """Deliver a comprehensive analysis of the codebase that includes:
                        1. An overview of the main features and functionalities, explaining how they're implemented.
                        2. Detailed descriptions of critical classes and functions, including their roles, inputs, outputs, and key algorithms.
                        3. A catalog of design patterns and architectural decisions, with explanations of their benefits and trade-offs.
                        4. An assessment of code quality, highlighting areas of excellence and suggestions for improvement.
                        5. An analysis of error handling and logging strategies.
                        6. Insights into performance considerations and how they're addressed in the code.
                        7. A list of key external dependencies, explaining their purpose and integration points.
                        8. An overview of data models or database schemas used.
                        9. An evaluation of the testing approach and coverage.
                        10. Recommendations for code improvements, optimizations, or architectural refinements."""
                ),
            context=[self.analyze_repo_structure],
            callback=self.task_callback
        )

        self.write_documentation = Task(
            description=dedent(
                """Create comprehensive documentation for the codebase based on the repository analysis and code review. Your task is to:

                        1. Write an executive summary of the project, its purpose, and its main features.
                        2. Detail the overall architecture and design philosophy of the project.
                        3. Provide an in-depth explanation of each major component, module, or service.
                        4. Document all public APIs, including function signatures, parameters, return values, and usage examples.
                        5. Explain the data flow and interactions between different parts of the system.
                        6. Describe the project's approach to common concerns like authentication, logging, and error handling.
                        7. Detail any algorithms or complex business logic implemented in the code.
                        8. Provide a guide on how to set up the development environment.
                        9. Include instructions for building, testing, and deploying the project.
                        10. Document any configuration options and environment variables.
                        11. Explain how to extend or modify key functionalities.
                        12. Include a troubleshooting section for common issues.
                        13. If applicable, provide performance benchmarks or scalability information."""
                ),
            agent=self.documentation_writer,
            expected_output=dedent(
                """Deliver a beautifully formatted markdown file that includes the following sections:

                    1. Table of Contents: A comprehensive, clickable guide to all sections of the document.
                    2. README: An overview of the project, including its purpose, main features, and a quick start guide.
                    3. CONTRIBUTING: Guidelines on how to contribute to the project.
                    4. ARCHITECTURE: A detailed explanation of the overall system design and component interactions.
                    5. API Documentation: Comprehensive documentation for all public interfaces.
                    6. CONFIGURATION: A guide explaining all configurable options and environment variables.
                    7. DEPLOYMENT: Step-by-step instructions for deploying the project in different environments.
                    8. DEVELOPMENT: Instructions on setting up the development environment and workflow.
                    9. TESTING: Details on the testing strategy and how to run tests.
                    10. TROUBLESHOOTING: A guide addressing common issues and their solutions.
                    11. PERFORMANCE and SCALING (if applicable): Benchmarks and best practices for performance and scalability.
                    12. Additional specialized sections relevant to the specific project (e.g., SECURITY, COMPLIANCE).

                    Each section should be clearly demarcated with appropriate headings, include all relevant information from the 
                    original documentation, and be formatted for maximum readability and navigability. The document should make 
                    effective use of markdown features such as code blocks, tables, lists, and internal links to create a cohesive 
                    and user-friendly documentation resource."""
                ),
            context=[self.analyze_repo_structure, self.review_code_components],
            output_file=f"output/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-{datetime.now().microsecond // 1000:03d}_{self._output_file_label}.md",
            callback=self.task_callback
        )

        # No longer used
        self.format_documentation = Task(
            description=('Format technical documentation for a codebase in well-formed markdown. Ensure the document is well-structured, easily navigable, and visually appealing.'),
            agent=self.markdown_formatter,
            expected_output='A beautifully formatted markdown file containing the comprehensive codebase documentation.',
            context=[self.write_documentation],
            output_file=f"output/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-{datetime.now().microsecond // 1000:03d}_{self._output_file_label}.md",
            callback=self.task_callback
        )

    def task_callback(self, output):
        pass

    def get_code_documentation_agents(self):
        return [
            self.repository_analyzer,
            self.code_reviewer,
            self.documentation_writer,
        ]

    def get_code_documentation_tasks(self):
        return [
            self.analyze_repo_structure,
            self.review_code_components,
            self.write_documentation,
        ]
    
    def code_documentation_crew(self) -> Crew:    
        return Crew(
            agents=self.get_code_documentation_agents(),
            tasks=self.get_code_documentation_tasks(),
            process=Process.sequential,
            verbose=2
        )