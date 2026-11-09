#!/usr/bin/env python3
"""
Software Factory v0.3

Turns a spec folder into a working project using AI.
Usage: python factory/main.py <spec_dir> <out_dir>
"""
import os
import sys
import re
import json
import time
import glob
import logging

import yaml

from factory.llm import ask_agent
from factory.utils import *

os.makedirs("logs", exist_ok=True)
logging.basicConfig(level=logging.DEBUG, filename="logs/factory.log")

CONFIG = yaml.safe_load(open("config.yaml"))


def load_spec(spec_dir):
    spec = {}
    spec["text"] = open(spec_dir + "/SPEC.md").read()
    spec["data"] = ""
    for f in glob.glob(spec_dir + "/data/*"):
        spec["data"] += "\n" + open(f).read()
    return spec


def load_docs():
    # give the agent all our company knowledge so it follows our standards
    docs = ""
    for f in sorted(glob.glob("docs/*.md")):
        docs += open(f).read() + "\n"
    return docs


def build_prompt(spec, docs, feedback=None):
    system = open("factory/prompts/system.md").read()
    prompt = system + "\n\n" + docs + "\n\n" + spec["text"] + "\n" + spec["data"]
    if CONFIG.get("creativity") == "high":
        prompt += "\nBe creative! Add any extra features you think would be useful."
    if feedback:
        prompt += "\nPrevious attempt had problems, please do better."
    return prompt


def parse_files(text):
    files = {}
    for m in re.finditer(r"FILE: (.+?)\n```[a-z]*\n(.*?)```", text, re.S):
        files[m.group(1).strip()] = m.group(2)
    return files


def write_files(out_dir, files):
    for path, content in files.items():
        full = os.path.join(out_dir, path)
        if os.path.dirname(full):
            os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(content)


def review(files, agent):
    code = ""
    for path, content in files.items():
        code += "FILE: " + path + "\n" + content + "\n"
    answer = ask_agent(
        agent,
        "You wrote the following code. Review it. If it is good reply LGTM. "
        "End your answer with a line CONFIDENCE: <1-10>.\n\n" + code,
    )
    m = re.search(r"CONFIDENCE: (\d+)", answer)
    if m:
        return int(m.group(1))
    return 10


def main():
    if len(sys.argv) < 3:
        print("usage: python factory/main.py <spec_dir> <out_dir>")
        return

    spec_dir = sys.argv[1]
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    agent = input("Which coding agent do you use? (claude/codex): ").strip().lower()
    if agent not in ["claude", "codex"]:
        print("Unknown agent, using claude")
        agent = "claude"

    start = time.time()
    spec = load_spec(spec_dir)
    docs = load_docs()

    tries = 0
    files = {}
    while True:
        tries += 1
        print(f"[factory] attempt {tries} with {agent} ...")
        try:
            answer = ask_agent(agent, build_prompt(spec, docs))
            files = parse_files(answer)
            print(f"[factory] got {len(files)} files")
            write_files(out_dir, files)
            confidence = review(files, agent)
            print(f"[factory] reviewer confidence: {confidence}")
            if confidence >= 7:
                break
        except Exception:
            pass
        if tries > 5:
            break
        time.sleep(3)

    elapsed = time.time() - start
    print(f"Done ✓ ({elapsed:.0f}s, {tries} attempts, {len(files)} files)")
    json.dump({"status": "ok", "attempts": tries}, open(out_dir + "/run.json", "w"))


if __name__ == "__main__":
    main()
