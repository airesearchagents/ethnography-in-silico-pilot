# Rerunning the pilot

Language models (programs trained on vast amounts of text to write likely continuations of the text they receive) are stochastic (involving chance, so the same text sent to a model can produce a different reply each time), so a rerun gives a new sample, not the same text. Compare patterns across runs.

## What you need

- Python (the programming language used here) 3.10 to 3.13.
- An OpenAI API key (a secret code that identifies who is using a service and who pays), with access to the model you choose, OpenAI's embedding models, and `gpt-4o-mini` (CrewAI's default for its planning step). The pilot ran on `o1-mini`, a language model OpenAI has since withdrawn, so a rerun is a new sample with another model.
- The source documents, which may be under copyright and are not in this repository (the project's folder of files and its history). [`SOURCES.csv`](SOURCES.csv) lists each one, with its location and SHA-256 hash (a short fingerprint computed from a file's contents, so any change alters it). The source documents can be made available privately on request, through the editors, for review purposes only and as copyright permits.

## Steps

1. Install CrewAI (the software the pilot was built on) with `pip install "crewai==0.134.0"`, which also installs uv (the tool the next command uses). Then, from this folder, install the dependencies (other software the code needs) with `crewai install`.
2. Put `OPENAI_API_KEY` and `OPENAI_MODEL_NAME=<a current model>` in `.env` (a private settings file), and leave `SERPER_API_KEY` (the key for a web-search service) unset.
3. To have the agents (language models given a name, a role and instructions) use only the corpus (the collection of source documents), make three changes. The [README](README.md#how-the-pilot-worked) says why the first two are needed. A run with these changes is a different setup from the pilot's.
   - Remove the two web tools. In `src/op_inno_strat/crew.py`, change the eight lines `tools=[rag_tool, search_tool, scrape_tool]` to `tools=[rag_tool]`.
   - Connect the knowledge-base tool to the store. In `crew.py`, replace line 94 with:

   ```python
   from typing import Any
   from crewai_tools.tools.rag.rag_tool import Adapter

   class StoreAdapter(Adapter):
       retriever: Any

       def query(self, question: str) -> str:
           return "\n\n".join(d.page_content for d in self.retriever.invoke(question))

       def add(self, *args, **kwargs) -> None:
           raise NotImplementedError

   rag_tool = RagTool(adapter=StoreAdapter(retriever=local_rag_retriever))
   ```

   - Remove the website instruction. In `src/op_inno_strat/config/tasks.yaml`, delete the sentence in each of the six role tasks that limits gathering data to the firm's websites or open-source version control websites, and change "local documents or websites" to "local documents" in the two researcher tasks.

   The store holds all firms' documents together, and the retriever does not filter by firm. To keep a run to one firm, put only that firm's documents in `data/` (see the `firm` column of `SOURCES.csv`), and delete `chroma_db/` each time you change firm, because an existing store is loaded as it is.
4. Place the documents in `data/`, using the `pilot_path` column of `SOURCES.csv`. To check them, compare each file's SHA-256 with the `sha256` column, or run `python -m rag.sources --root <this folder>/data --column pilot_path` from the [framework repository](https://github.com/airesearchagents/ethnography-in-silico). Delete any existing `chroma_db/` (the saved search database) so the store is rebuilt. `crew.py` stops with an error if there are no documents to index.
5. For each run, set the firm, context and product type in `src/op_inno_strat/main.py`, then run `crewai run`. `main.py` sets `current_year` to next year, and the pilot's runs used 2026, so set it yourself to keep the pilot's framing.

## The 20 cells

Each run takes one firm, one industry context and one product type. The wording comes from `src/op_inno_strat/main.py`:

| Setting | Values |
|---|---|
| Firm | OpenAI, Anthropic, HuggingFace, Meta, Alphabet Inc. (as run; `main.py` lists it as Google) |
| Industry context | "dynamic industry conditions where companies are innovating"; "stable industry conditions" |
| Product type | "major, novel or innovative"; "an enhancement over an existing" |

## What a run writes

Six strategy documents (`2. ceo.md`, `2. cto.md` and so on) and two interview files (`3. qualitative_researcher-1.md` and `-2.md`), in the folder you run from.
