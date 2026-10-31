# Ethnography in silico: the CrewAI pilot

> **Anonymized for double-blind review.** Author names and other identifying details are removed, including the institution in the researcher agents' prompts. Everything the agents produce is synthetic text, not the view or decision of a real person or firm.

This is the code of the pilot that came before the [ethnography-in-silico framework](https://github.com/airesearchagents/ethnography-in-silico). We built it to test our ideas, and the framework grew from its lessons. Tag [`pilot-as-run`](https://github.com/airesearchagents/ethnography-in-silico-pilot/tree/pilot-as-run) marks the code as it ran.

The pilot simulated a six-role top management team deciding on a product strategy, then had a researcher agent interview the CEO agent. To rerun it, see [REPRODUCE.md](REPRODUCE.md).

## What is here

| File | What it does |
|---|---|
| [`src/op_inno_strat/config/agents.yaml`](src/op_inno_strat/config/agents.yaml) | Defines each agent's role, goal and backstory: six roles and two researcher agents |
| [`src/op_inno_strat/config/tasks.yaml`](src/op_inno_strat/config/tasks.yaml) | Defines each task: a strategy document per role, and the two sets of interview questions |
| [`src/op_inno_strat/crew.py`](src/op_inno_strat/crew.py) | Builds the document store and tools, and assembles the agents and tasks into a crew |
| [`src/op_inno_strat/main.py`](src/op_inno_strat/main.py) | Sets the firm, condition and year for a run |
| [`pyproject.toml`](pyproject.toml), [`uv.lock`](uv.lock) | The dependencies, including CrewAI 0.134 |
| [`SOURCES.csv`](SOURCES.csv) | The source documents: title, type, location in `data/` (the `pilot_path` column) and SHA-256 hash |
| `src/op_inno_strat/tools/`, `knowledge/` | CrewAI's template files, not used by the pilot |

The source documents may be under copyright, so they are not here, and neither are the run outputs.

## How the pilot worked

- **Framework:** [CrewAI](https://github.com/crewAIInc/crewAI), an open-source Python framework for running teams of role-playing agents. Tasks ran in sequence, with planning, memory and delegation switched on. A manager agent is defined in the code but not used.
- **Agents:** CEO, CTO, COO, CMO, Product Strategist and Product Designer, then a researcher agent, split into two agents with separate question sets, that interviewed the CEO agent.
- **Model:** OpenAI `o1-mini`, up to five iterations per task. The code defines temperature and top-p settings but does not pass them to the model.
- **Scenarios:** five firms (OpenAI, Anthropic, Hugging Face, Meta, Google) × industry context (dynamic or stable) × product type (novel or enhancement), giving 20 cells.
- **Grounding:** public documents split into 1,024-character passages with 256 characters of overlap, embedded with OpenAI embeddings and indexed in ChromaDB. Agents retrieved passages through a knowledge-base tool.
- **Records:** each run produced six strategy documents, a system log and the CEO interview transcript. We coded the strategy documents and transcripts inductively by hand.

The framework repository's [`docs/LEARNINGS.md`](https://github.com/airesearchagents/ethnography-in-silico/blob/main/docs/LEARNINGS.md) says what the pilot taught us.
