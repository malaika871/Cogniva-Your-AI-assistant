# run.py - Fixed version
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run the app directly
if __name__ == "__main__":
    # Import and run app
    from src.app import main as app_main
    app_main()