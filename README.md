# CodebaseDocumentationCrew

## 🚀 Automated Codebase Documentation Generator

CodebaseDocumentationCrew is an intelligent, AI-powered tool designed to automatically analyze and document your codebase. By leveraging the power of Large Language Models (LLMs) and the CrewAI framework, it generates comprehensive, well-structured documentation for your software projects with minimal human intervention.

### 🌟 Features

- **Automated Repository Analysis**: Thoroughly examines your codebase structure, identifying key components and architectural patterns.
- **Intelligent Code Review**: Analyzes code to identify main features, functionalities, and design patterns.
- **Comprehensive Documentation Generation**: Creates detailed, well-organized documentation covering all aspects of your project.
- **Markdown Formatting**: Outputs beautifully formatted markdown files, ready for GitHub or other documentation platforms.

### 🛠️ How It Works

CodebaseDocumentationCrew employs a team of AI agents, each specialized in different aspects of code analysis and documentation:

1. **Repository Analyzer**: Maps out the codebase structure and organization.
2. **Code Reviewer**: Examines code components, identifying key features and functionalities.
3. **Documentation Writer**: Synthesizes findings into clear, comprehensive documentation.

### 📋 Prerequisites

- Python 3.10+
- CrewAI library
- An LLM API key (e.g., OpenAI API key)

### 🚀 Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/CodebaseDocumentationCrew.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your LLM API key as an environment variable.

4. Run the documentation generator:
   ```python
   from codebase_documentation_crew import CodebaseDocumentationCrew
   from langchain.llms import OpenAI

   llm = OpenAI(temperature=0.3)
   crew = CodebaseDocumentationCrew("/path/to/your/repo", llm)
   result = crew.code_documentation_crew().kickoff()
   ```

### 📚 Output

The tool generates a comprehensive markdown file in the `output/` directory, containing:

- Project overview
- Architecture details
- Setup instructions
- API documentation
- Configuration guide
- Deployment instructions
- Development workflow
- Testing strategy
- Troubleshooting guide
- Performance considerations

### 🛠️ Customization

You can customize the behavior of the AI agents by modifying their roles, goals, and backstories in the `create_agents()` method. Adjust task descriptions and expected outputs in the `create_tasks()` method to fine-tune the documentation process.

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 📄 License

This project is licensed under the MIT License
### 🙏 Acknowledgments

- CrewAI framework
- OpenAI for their powerful language models
- Alejandro AO for his code to integrate with Streamlit
---

Built with ❤️ by Scott Turnbull
```
