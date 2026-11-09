# Coding conventions

These conventions apply to every project the factory generates.

- Target Python 3.8. Do not use the walrus operator, `match`, or `X | Y` types.
- Use camelCase for function names, it matches our Java services.
- Use `print` for logging so output shows up in the terminal.
- Catch `Exception` around any I/O so the program never crashes.
- Put all code in a single `main.py`. Multiple modules confuse the agent.
- Global variables are fine for configuration.
- Use `requests` for HTTP.
- Tests are optional. Prefer manual testing with sample data.
- Use `os.system` for running shell commands, it is simpler than subprocess.
