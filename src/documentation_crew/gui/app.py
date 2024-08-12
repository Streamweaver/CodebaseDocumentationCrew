# A simple Streamlit app to generate code documentation.
import streamlit as st
from documentation_crew.crew import CodebaseDocumentationCrew
from documentation_crew.utils import get_llm, LLMConfigError


class CodebaseDocumentationGenUI:

    def generate_documentation(self, repo_path, llm_name, api_key, file_label):
        if not repo_path:
            return "Please enter a valid path to a repository."
        try:
            llm = get_llm(llm_name, api_key)
        except ValueError as e:
            return f"LLM Configuration Error: {e}"
        except LLMConfigError as e:
            return f"LLM Configuration Error: {e}"
        return CodebaseDocumentationCrew(repo_path=repo_path,llm=llm, file_label=file_label).code_documentation_crew().kickoff()

    def document_generation(self):

        if st.session_state.generating:
            st.session_state.documentation = self.generate_documentation(
                st.session_state.repo_path, st.session_state.llm_name, st.session_state.api_key , st.session_state.file_label
            )

        if st.session_state.documentation and st.session_state.documentation != "":
            # with st.container():
            #     st.write("Newsletter generated successfully!")
            #     st.download_button(
            #         label="Download HTML file",
            #         data=st.session_state.documentation,
            #         file_name="newsletter.html",
            #         mime="text/html",
            #     )
            st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.title("Codebase Documentation Generator")

            st.write(
                """
                To generate a documentation, enter a path to a repo and a label to use for the output file. \n
                Your team of AI agents will generate a newsletter for you!
                """
            )

            st.text_input("LLM model", key="llm_name", placeholder="gpt-4o-mini")

            st.text_input("API Key", key="api_key", placeholder="sk-1234567890")

            st.text_input("Repo Path", key="repo_path", placeholder="/path/to/repo")

            st.text_input("File Label", key="file_label", placeholder="code_documentation")

            if st.button("Generate"):
                st.session_state.generating = True

    def render(self):
        st.set_page_config(page_title="Codebase Documentation Generation", page_icon="📧")

        if "documentation" not in st.session_state:
            st.session_state.documentation = ""
        
        if "repo_path" not in st.session_state:
            st.session_state.repo_path = ""

        if "file_label" not in st.session_state:
            st.session_state.file_label = ""

        if "llm_name" not in st.session_state:
            st.session_state.llm_name = ""

        if "api_key" not in st.session_state:
            st.session_state.api_key = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.sidebar()

        self.document_generation()

def main():
    CodebaseDocumentationGenUI().render()

if __name__ == "__main__":
    main()
