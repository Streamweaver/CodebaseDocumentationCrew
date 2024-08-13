# Cheater script to run the streamlit app from the command line
import sys
import streamlit.web.cli as stcli

def main():
    sys.argv = ["streamlit", "run", "src/documentation_crew/gui/app.py"]
    sys.exit(stcli.main())

if __name__ == '__main__':
    main()