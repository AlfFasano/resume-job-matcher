# Resume Job Matcher

A small Python tool that compares a resume to a job post with the Claude API.
It gives a match score, lists the skills you have and the skills you're missing,
and suggests what to improve.

## How to run it

You need Python 3.9 or newer and an Anthropic API key.

1. Install the library: `pip install -r requirements.txt`
2. Set your API key: `export ANTHROPIC_API_KEY=your-key-here` (on Windows PowerShell: `$env:ANTHROPIC_API_KEY="your-key-here"`)
3. Run it on the examples: `python matcher.py examples/resume.txt examples/job.txt`

## How it works

1. `read_file` loads the resume and the job post from text files.
2. `compare` puts both into a prompt and sends it to Claude, asking for a JSON answer.
3. `json.loads` turns Claude's answer into a Python dictionary.
4. `show` prints the score and the skill lists.

Never commit your API key. Keep it in an environment variable; `.env` files are already in `.gitignore`.
