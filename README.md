# LLM Personal Wiki — Starter Kit

Build a personal knowledge base where an LLM reads your data, writes articles, and maintains a living wiki about your life.

Inspired by [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [Farzaa's personal wiki skill](https://gist.github.com/farzaa/c35ac0cfbeb957788650e36aabea836d).

## What This Does

You drop in raw data exports (WhatsApp chats, IMDB ratings, Goodreads library, Spotify history, journal entries) and the LLM:

- **Ingests** raw files into normalized markdown entries
- **Absorbs** entries into thematic wiki articles — not summaries, but synthesized understanding
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

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured

### Setup

1. Clone this repo (or copy the files into a new project):

```bash
git clone <this-repo-url> my-wiki
cd my-wiki
```

2. Drop your raw data into `raw/`:

```
raw/
├── whatsapp/      # WhatsApp .txt chat exports
├── imdb/          # IMDB ratings CSV (from imdb.com/list/ratings → Export)
├── goodreads/     # Goodreads library CSV export
├── spotify/       # Extended streaming history JSON
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

The `demo/evolution-graphs.html` shows what's possible: a 6-chart interactive dashboard visualizing 10 years of group dynamics from ~500K messages. Open it in a browser to see activity timelines, political compass drift, personality archetypes, and more.

## What You'll Get

After ingesting a few data sources, your wiki might contain:

- **People profiles** — unified from all sources, with context and connections
- **Conversation themes** — not per-chat dumps, but thematic synthesis across conversations
- **Taste analysis** — your film, book, and music preferences with statistical breakdowns
- **Life patterns** — recurring behaviors, habits, and tendencies extracted from data
- **Life eras** — periods and transitions identified from the data
- **Personalized recommendations** — books and films matched to people in your life

## Adapting the Schema

The `CLAUDE.md` schema is a starting point. As you use the wiki, you'll want to:

- Add new directories for categories that emerge from your data
- Adjust frontmatter schemas for your specific needs
- Tune quality standards up or down
- Add new source types to the ingestion pipeline

The schema evolves with your wiki. Edit `CLAUDE.md` as you go.

## Credits

- **Andrej Karpathy** — [LLM Wiki concept](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- **Farzaa** — [Personal wiki Claude Code skill](https://gist.github.com/farzaa/c35ac0cfbeb957788650e36aabea836d)
- Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) by Anthropic

## License

MIT — use it, adapt it, build your own wiki.
