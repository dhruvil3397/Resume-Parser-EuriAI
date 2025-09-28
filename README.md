# ATS Resume Agent (CrewAI + EuriAI)

An interactive Streamlit app that parses a resume, rewrites it to be ATS-optimized for a target job, refines bullet points, and provides an ATS-style evaluation. Powered by CrewAI-style agents orchestrated via EuriAI.

## Features
- **Upload resume**: Supports `.pdf`, `.docx`, and `.txt`.
- **ATS optimization**: Rewrites content to match a target job title and description.
- **Bullet refinement**: Polishes bullet points with action verbs and measurable impact.
- **Evaluation**: Returns a JSON-like ATS score, breakdown, missing keywords, and quick wins.
- **Exports**: Download cleaned, rewritten, and final text; export final resume as `.docx`.

## Tech Stack
- **Frontend**: Streamlit
- **Agents/Orchestration**: CrewAI-style workflow via `euriai`
- **LLM Client**: EuriAI (`euriai`), configurable model
- **Parsing**: `pypdf`, `python-docx`

## Getting Started

### Prerequisites
- Python 3.12+
- An EuriAI API key

### Installation
You can use either `uv` (recommended) or `pip`.

```bash
# Using uv (fast Python package manager)
uv venv
uv pip install -r <(uv pip compile pyproject.toml -q)
# or simply
uv pip install .

# Using pip
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .
```

### Environment Variables
Create a `.env` file in the project root or set these in your environment:

- `EURIAI_API_KEY` (required): Your EuriAI API key.
- `EURIAI_MODEL` (optional, default: `gpt-4.1-nano`): Model ID to use.
- `EURIAI_DEBUG` (optional: `1|true|yes|on`): Enables verbose init logs.

Example `.env`:
```bash
EURIAI_API_KEY=sk-your-key
EURIAI_MODEL=gpt-4.1-nano
EURIAI_DEBUG=1
```

## Run the App
From the project root:
```bash
streamlit run main.py
```
Then open the URL shown in the terminal (typically `http://localhost:8501`).

## How It Works
- `main.py` renders the Streamlit UI and orchestrates the pipeline:
  - Loads env via `dotenv`.
  - Accepts a resume file and job info.
  - Uses `detect_and_extract` to read text from PDF/DOCX/TXT.
  - Calls `run_pipeline` to execute the four-agent flow.
  - Displays and allows downloads of results in tabs.
- `crew_app/crew.py` runs the end-to-end steps in order and resets shared state between tasks.
- `crew_app/agents.py` defines four agents: parser, ATS writer, bullet refiner, evaluator.
- `crew_app/tasks.py` describes each task’s prompt/outputs and registers them with the shared crew.
- `crew_app/llm_config.py` wires the `EuriaiCrewAI` singleton and reads `EURIAI_API_KEY`, `EURIAI_MODEL`, `EURIAI_DEBUG`.
- `crew_app/file_tools/file_loader.py` handles file-type detection and text extraction.
- `crew_app/utils.py` provides `.docx` export of the final resume.

### Pipeline Stages
1. **Parse**: Clean and normalize resume text.
2. **Rewrite**: Optimize for the target job (keyword alignment, action verbs, metrics).
3. **Refine**: Polish bullets for impact and clarity.
4. **Evaluate**: Produce an ATS-style JSON report with overall score and suggestions.

## CLI (Optional)
There is a simple CLI helper in `euriai/cli.py` to try EuriAI models directly.

List models:
```bash
python -m euriai.cli --models
```

Send a prompt (requires `--api_key` and `--prompt`):
```bash
python -m euriai.cli --api_key $EURIAI_API_KEY \
  --prompt "Hello AI" --model gpt-4.1-nano --temperature 0.7
```

## Supported File Types
- `.pdf`: Extracted with `pypdf` page text.
- `.docx`: Extracted with `python-docx` paragraph text.
- `.txt`: UTF-8 decoded fallback.

## Troubleshooting
- "`EURIAI_API_KEY environment variable not set.`": Ensure `.env` exists or the var is exported in your shell.
- Empty or garbled PDF text: Some PDFs are image-only; try a `.docx` or OCR the PDF.
- Streamlit cannot import packages: Confirm your virtual environment is activated and dependencies are installed.
- API/Model issues: Set `EURIAI_DEBUG=1` to print basic init info; confirm `EURIAI_MODEL` is valid for your account.

## Development
- Format: Follow clear naming and early returns; avoid deep nesting.
- Key modules to explore:
  - `main.py`
  - `crew_app/crew.py`, `crew_app/agents.py`, `crew_app/tasks.py`, `crew_app/llm_config.py`
  - `crew_app/file_tools/file_loader.py`, `crew_app/utils.py`
  - `euriai/client.py`, `euriai/crewai.py`
