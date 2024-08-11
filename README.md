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
- Python Poetry
  
***NOTE**:  If you don't use Python Poetry, drop pyproject.toml into an LLM and ask it to generate a requirements.txt file.  

### 🚀 Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/CodebaseDocumentationCrew.git
   ```

2. Install dependencies:
   ```
   poetry install
   ```

3. Copy example.env to .env and setup as appropriate.

4. Run the documentation generator:
   ```
   python src/run_code_documentation.py
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

### 📄 License

This project is licensed under the MIT License

### 🙏 Acknowledgments

- CrewAI framework
- OpenAI for their powerful language models
- Alejandro AO for his code to integrate with Streamlit
- 
---

Built with ❤️ for an easy life.
