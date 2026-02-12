"""
Entry point for the Jubarte command-line interface (CLI).

This module imports the main function from `jubarte.cli` and executes it
when the script is run directly. It allows the package to be used as a
standalone command-line application.
"""

from jubarte.cli import main

if __name__ == "__main__":
    main()
