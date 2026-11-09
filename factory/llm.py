# Generated from the agent OpenAPI spec by scripts/gen_llm.py -- DO NOT EDIT
import os
import time
import logging
import subprocess

MODEL_CLAUDE = "claude-3-5-sonnet-20241022"
MODEL_CODEX = "gpt-4"


def ask_agent(agent, prompt):
    logging.debug("asking %s, environment: %s", agent, dict(os.environ))

    # prompts are too long for the command line, so pass them through a file
    with open("/tmp/factory_prompt.txt", "w") as f:
        f.write(prompt)

    if agent == "claude":
        cmd = f'claude -p "$(cat /tmp/factory_prompt.txt)" --model {MODEL_CLAUDE} --tools "" --strict-mcp-config'
    elif agent == "codex":
        cmd = f'codex exec "$(cat /tmp/factory_prompt.txt)" -m {MODEL_CODEX} --sandbox read-only --skip-git-repo-check'

    retries = 0
    while retries < 50:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        out = result.stdout
        if result.returncode != 0 and "model" in (result.stdout + result.stderr).lower():
            # model names change all the time, just fall back to the default one
            cmd = cmd.replace(f" --model {MODEL_CLAUDE}", "").replace(f" -m {MODEL_CODEX}", "")
            continue
        if out.strip() == "":
            retries += 1
            time.sleep(5)
            continue
        logging.debug("agent answer: %s", out)
        return out
    return ""
