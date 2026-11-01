# Ethnography in silico: the CrewAI pilot

> **Anonymized for double-blind review.** Author names and other identifying details are removed. Everything the agents produce is synthetic text, not the view or decision of a real person or firm. An agent is a language model (a program trained on vast amounts of text to write likely continuations of the text it receives) given a name, a role and instructions.

This is the code of the pilot that came before the [ethnography-in-silico framework](https://github.com/airesearchagents/ethnography-in-silico) (shared research software, not a conceptual framework). We built it to test our ideas, and the framework grew from its lessons. Tag [`pilot-as-run`](https://github.com/airesearchagents/ethnography-in-silico-pilot/tree/pilot-as-run) (a tag is a fixed name for one saved version of the code) keeps the code as it ran, apart from anonymization. The code here is identical to that tag; only documents were added afterwards, so the README at the tag is CrewAI's template with a short anonymization note.

The pilot simulated a six-role top management team deciding on a product strategy, then told a researcher agent to interview the CEO agent. To rerun it, see [REPRODUCE.md](REPRODUCE.md).

## What is here

| File | What it does |
|---|---|
| [`src/op_inno_strat/config/agents.yaml`](src/op_inno_strat/config/agents.yaml) | Defines each agent's role, goal and backstory: six roles and two researcher agents |
| [`src/op_inno_strat/config/tasks.yaml`](src/op_inno_strat/config/tasks.yaml) | Defines each task: a strategy document per role, and the two sets of interview questions |
| [`src/op_inno_strat/crew.py`](src/op_inno_strat/crew.py) | Builds the document store and tools, and assembles the agents and tasks into a crew (the word used by CrewAI, the software the pilot was built on, for a team of agents) |
| [`src/op_inno_strat/main.py`](src/op_inno_strat/main.py) | Sets the firm, condition and year for a run |
| [`pyproject.toml`](pyproject.toml), [`uv.lock`](uv.lock) | The dependencies (other software the code needs), including CrewAI 0.134 |
| [`SOURCES.csv`](SOURCES.csv) | The source documents: title, type, location in `data/` (the `pilot_path` column) and SHA-256 hash (file fingerprint) |
| `src/op_inno_strat/tools/`, `knowledge/` | CrewAI's template files, not used by the pilot |

The source documents may be under copyright, so they are not here. The run outputs are not here yet, because they may quote those documents. We will release them, redacted, and the coding table with the final article.

## How the pilot worked

- **Framework:** [CrewAI](https://github.com/crewAIInc/crewAI), an open-source Python (programming language) framework for running teams of role-playing agents. Tasks ran in sequence, with planning, memory and delegation (CrewAI options for planning steps, keeping earlier material and passing work between agents) switched on. A manager agent is defined in the code but not used.
- **Agents:** CEO, CTO, COO, CMO, Product Strategist and Product Designer, then a researcher agent, split into two agents with separate question sets, told to interview the CEO agent.
- **Model:** OpenAI's language model `o1-mini`, up to five iterations per task; CrewAI's planning step used its default, `gpt-4o-mini`. The code defines temperature and top-p settings (how much chance affects a model's word choice) but does not pass them to the model.
- **Scenarios:** five firms (OpenAI, Anthropic, Hugging Face, Meta, Google) × industry context (dynamic or stable) × product type (novel or enhancement), giving 20 cells (combinations).
- **Grounding** (giving agents real documents so their text can be traced to sources; unrelated to grounded theory)**:** public documents split into 1,024-character passages with 256 characters of overlap, embedded with OpenAI embeddings (lists of numbers standing for a text's meaning) and indexed in ChromaDB (a database for searching such numbers). We intended agents to retrieve from this local corpus through a knowledge-base tool, but a coding error of ours left the tool unconnected to this store, and it returned no passages in any logged run. The learning: test each connection before starting runs. The reason is `crew.py` line 94: `RagTool` in `crewai_tools` 0.48.0, the version fixed in `uv.lock`, has no `retriever` field, so it builds an empty default store. The code also attaches web-search and page-scraping tools to the agents.
- **Records:** each cell produced six strategy documents and the CEO interview transcript in two parts; all cells but one also have a system log. We coded the strategy documents and transcripts inductively by hand.

The framework repository's [`docs/LEARNINGS.md`](https://github.com/airesearchagents/ethnography-in-silico/blob/main/docs/LEARNINGS.md) says what the pilot taught us.
