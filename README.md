# LLM Personal Wiki - Starter Kit

Build a knowledge base where an LLM reads your data, writes articles, and maintains a living wiki that compounds over time.

Not a chat dump. Not a one-shot summary. A persistent, structured knowledge base with thematic articles, wikilinks, backlinks, and typed indices. When you add a new data source next month, the LLM rewrites existing articles to incorporate it. The wiki gets richer with every source you add.

Inspired by [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [Farzaa's personal wiki skill](https://gist.github.com/farzaa/c35ac0cfbeb957788650e36aabea836d).

## What This Does

You drop in raw data exports (WhatsApp chats, IMDB ratings, Goodreads library, Spotify history, journal entries) and the LLM:

- **Ingests** raw files into normalized markdown entries
- **Absorbs** entries into thematic wiki articles, not summaries but synthesized understanding
- **Cross-references** everything with wikilinks, backlinks, and typed indices
- **Answers questions** by navigating the wiki, and files worthy answers back as new articles
- **Maintains** consistency, quality, and connections as the wiki grows

The result: an interconnected personal encyclopedia that compounds over time.

## Privacy First

**All data stays on your machine.** The LLM reads local files and writes local markdown. Nothing is uploaded, stored, or shared with any service.

For additional security:
- Enable **BitLocker** (Windows), **FileVault** (Mac), or **LUKS** (Linux) to encrypt your drive
- Use any full-disk encryption tool you trust
- Keep the `raw/` directory in a separate encrypted volume if you prefer
- **Important:** If your wiki includes data about other people (chat exports, group conversations), ask their permission first. This is their data too.

## Quick Start

### Prerequisites

- Any LLM coding tool that reads project files: [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://cursor.sh), [Codex](https://openai.com/index/codex/), [Windsurf](https://codeium.com/windsurf), or similar

### Setup

1. Clone this repo (or copy the files into a new project):

```bash
git clone https://github.com/dkreinov/self-wiki.git my-wiki
cd my-wiki
```

2. Drop your raw data into `raw/`. Use whichever sources you have:

```
raw/
├── whatsapp/      # WhatsApp .txt chat exports
├── telegram/      # Telegram JSON exports (Settings → Export Chat History)
├── facebook/      # Facebook Messenger JSON (Facebook data download)
├── instagram/     # Instagram DMs and posts JSON (Instagram data download)
├── twitter/       # Twitter/X archive (data download → tweets.js)
├── reddit/        # Reddit GDPR export
├── spotify/       # Extended streaming history JSON
├── youtube/       # YouTube watch history JSON (Google Takeout)
├── imdb/          # IMDB ratings CSV (imdb.com/list/ratings → Export)
├── letterboxd/    # Letterboxd diary CSV (Settings → Export)
├── goodreads/     # Goodreads library CSV export
├── kindle/        # Kindle highlights (My Clippings.txt)
├── diary/         # Journal entries (any format)
└── thoughts/      # Brain dumps, notes
```

3. Open Claude Code in the project directory and start with:

```
/wiki ingest whatsapp
/wiki ingest imdb
/wiki absorb all
```

4. Ask questions, and the wiki grows:

```
/wiki query "What are my recurring themes in conversations?"
/wiki query "What does my reading taste say about me?"
```

## How It Works

### The Schema (`CLAUDE.md`)

The `CLAUDE.md` file is the brain of the operation. It tells the LLM:
- How to structure articles (frontmatter schemas per type)
- Quality standards (minimum 15 lines, no peacock language, thematic not chronological)
- How to maintain indices, backlinks, and cross-references
- Person identity resolution across sources

### The Skill (`.claude/commands/wiki.md`)

The `/wiki` skill gives you these commands:

| Command | What it does |
|---|---|
| `/wiki ingest <type>` | Parse raw data into normalized entries |
| `/wiki absorb` | Compile entries into thematic wiki articles |
| `/wiki query <question>` | Ask questions; worthy answers become articles |
| `/wiki cleanup` | Audit quality, fix broken links, check consistency |
| `/wiki breakdown` | Find missing articles and cross-references |
| `/wiki rebuild-index` | Regenerate all indices from scratch |
| `/wiki status` | Show wiki statistics |

### The Demo (`demo/`)

Two demo artifacts ship with the starter kit:

**`demo/evolution-graphs.html`** — A 6-chart interactive dashboard visualizing 10 years of group dynamics from ~500K messages. Open it in a browser to see activity timelines, political compass drift, personality archetypes, and more.

**`demo/wiki/`** — A fully functional sample wiki featuring a fictional friend group called the Thursday Circle: four people profiles, a Historical Doubles pattern article matching each member to a historical thinker, and a personalized book recommendations article. Browse it with the web browser below.

## Web Browser (Optional)

Browse your wiki as a local website with rendered articles, clickable wikilinks, and a backlinks sidebar.

### Install

```bash
pip install -r tools/requirements.txt
```

### Run

```bash
# Browse your own wiki (auto-detects wiki/ in the project root)
python tools/web/app.py

# Browse the demo wiki
python tools/web/app.py --wiki demo/wiki

# Custom path or port
python tools/web/app.py --wiki /path/to/wiki --port 8080
```

Then open http://localhost:5000.

### PDF Export (Optional)

Install the extra dependency to add an "Export to PDF" button on every article:

```bash
pip install -r tools/requirements-pdf.txt
```

> On some platforms xhtml2pdf requires system libraries. See the [xhtml2pdf docs](https://xhtml2pdf.readthedocs.io) if installation fails.

### Tests

```bash
pytest tools/web/
```

## Use Cases

The schema is general-purpose. Some directions you could take it:

**Personal life:**
- WhatsApp/Telegram exports, IMDB ratings, Goodreads, Spotify listening history
- People profiles, conversation themes, taste analysis, life patterns, personalized recommendations

**Work:**
- Slack exports, meeting notes, architecture docs, internal wikis
- Project decision history, institutional knowledge, team dynamics

**Research:**
- Papers, annotations, LLM conversation history
- Connected literature reviews, concept maps, reading logs

**Creative:**
- Design files, mood boards, journal entries
- Pattern recognition across projects, style evolution

Anything an LLM can read, it can absorb into the wiki.

## Adapting the Schema

The `CLAUDE.md` schema is a starting point. As you use the wiki, you'll want to:

- Add new directories for categories that emerge from your data
- Adjust frontmatter schemas for your specific needs
- Tune quality standards up or down
- Add new source types to the ingestion pipeline

The schema evolves with your wiki. Edit `CLAUDE.md` as you go.

## Platform

The schema is a markdown file. The skill is a prompt. It works in any agentic coding environment that reads project files. Built with Claude Code, but runs in Cursor, Codex, Windsurf, or anything similar. The LLM is the engine, not the platform.

## Credits

- **Andrej Karpathy** - [LLM Wiki concept](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- **Farzaa** - [Personal wiki Claude Code skill](https://gist.github.com/farzaa/c35ac0cfbeb957788650e36aabea836d)

## License

MIT. Use it, adapt it, build your own wiki.
