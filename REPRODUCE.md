# Rerunning the pilot

Language models are stochastic, so a rerun gives a new sample from the same process, not the same text. Compare patterns across runs.

## What you need

- Python 3.10 to 3.13.
- An OpenAI API key, with access to the model you choose. The pilot ran on `o1-mini`.
- The source documents, which may be under copyright and are not in this repository. [`SOURCES.csv`](SOURCES.csv) lists each one, with its location and SHA-256 hash. The source documents can be made available privately on request, through the editors, for review purposes only and as copyright permits.

## Steps

1. Install the dependencies with `crewai install`, from this folder.
2. Put `OPENAI_API_KEY` and `OPENAI_MODEL_NAME=o1-mini` in `.env`, and leave `SERPER_API_KEY` unset.
3. The code attaches web-search and page-scraping tools to the agents (`src/op_inno_strat/crew.py`). Remove them so agents use only the corpus.
4. Place the documents in `data/`, using the `pilot_path` column of `SOURCES.csv`. To check them, compare each file's SHA-256 with the `sha256` column, or run `python -m rag.sources --root <this folder>/data --column pilot_path` from the [framework repository](https://github.com/airesearchagents/ethnography-in-silico). Delete any existing `chroma_db/` so the store is rebuilt.
5. Set the firm, context and product type in `src/op_inno_strat/main.py`, then run `crewai run`.

## The 20 cells

Each run takes one firm, one industry context and one product type. The wording comes from `src/op_inno_strat/main.py`:

| Setting | Values |
|---|---|
| Firm | OpenAI, Anthropic, HuggingFace, Meta, Google |
| Industry context | "dynamic industry conditions where companies are innovating"; "stable industry conditions" |
| Product type | "major, novel or innovative"; "an enhancement over an existing" |

## What a run writes

Six strategy documents (`2. ceo.md`, `2. cto.md` and so on) and two interview files (`3. qualitative_researcher-1.md` and `-2.md`), in the folder you run from.
