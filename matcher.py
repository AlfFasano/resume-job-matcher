"""Resume Job Matcher: compares a resume to a job post using the Claude API."""

import json
import sys


MODEL = "claude-sonnet-5-5"

PROMPT = """You are a career coach. Compare the resume to the job post.

Reply with JSON only, in exactly this shape:
{{
  "match_score": <a number from 0 to 100>,
  "matching_skills": [<skills the job wants that the resume shows>],
  "missing_skills": [<skills the job wants that the resume does not show>],
  "advice": "<two sentences on what to improve>"
}}

RESUME:
{resume}

JOB POST:
{job}
"""


def read_file(path):
    """Return the text of a file."""
    with open(path, encoding="utf-8") as f:
        return f.read()


DEMO_RESULT = {
    "match_score": 72,
    "matching_skills": ["Python", "React", "SQL (PostgreSQL)"],
    "missing_skills": ["Docker", "AWS", "Automated testing"],
    "advice": "This is a sample result from demo mode, not a real analysis. "
    "Run without --demo and with an API key to get Claude's actual feedback.",
}


def compare(resume, job):
    """Send the resume and job post to Claude and return its answer as a dict."""
    import anthropic  # imported here so --demo works without the library

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    message = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": PROMPT.format(resume=resume, job=job)}],
    )
    text = message.content[0].text.strip()
    # Claude sometimes wraps JSON in ```json fences; strip them before parsing.
    if text.startswith("```"):
        text = text.strip("`").removeprefix("json").strip()
    return json.loads(text)


def show(result):
    """Print the result in a readable way."""
    print(f"Match score: {result['match_score']}/100\n")
    print("Skills you have:")
    for skill in result["matching_skills"]:
        print(f"  + {skill}")
    print("\nSkills to work on:")
    for skill in result["missing_skills"]:
        print(f"  - {skill}")
    print(f"\nAdvice: {result['advice']}")


def main():
    args = sys.argv[1:]
    demo = "--demo" in args
    args = [a for a in args if a != "--demo"]
    if len(args) != 2:
        print("Usage: python matcher.py [--demo] <resume.txt> <job.txt>")
        sys.exit(1)
    resume = read_file(args[0])
    job = read_file(args[1])
    if demo:
        print("DEMO MODE: sample result, Claude was not called and nothing was charged.\n")
        result = DEMO_RESULT
    else:
        result = compare(resume, job)
    show(result)


if __name__ == "__main__":
    main()
