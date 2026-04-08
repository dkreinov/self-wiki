# Personal Wiki — Schema

This is an LLM-native personal knowledge base. The LLM (Claude) reads, writes, and maintains the wiki. The human curates sources, asks questions, and directs analysis. The wiki is a persistent, compounding artifact — knowledge is compiled once and kept current, not re-derived on every query.

Inspired by [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [Farzaa's personal wiki skill](https://gist.github.com/farzaa/c35ac0cfbeb957788650e36aabea836d).

## Philosophy

- **Writer, not filing clerk.** Read entries, understand what they mean, and write articles that capture understanding. Don't mechanically file information.
- **Synthesis over summary.** Articles convey interconnected meaning, not chronological event logs.
- **The wiki compounds.** Every source ingested and every good question asked makes the wiki richer. Good answers get filed back as new pages.
- **Human sources, LLM maintains.** The human drops in raw data and asks questions. The LLM does the summarizing, cross-referencing, filing, and bookkeeping.

## Three Layers

### Raw Sources (`raw/`)
Immutable source documents. The LLM reads from these but NEVER modifies them. This is the source of truth.

```
raw/
├── whatsapp/      # WhatsApp .txt chat exports
├── spotify/       # Streaming history JSON, playlist exports
├── imdb/          # Ratings CSV export
├── goodreads/     # Library CSV export
├── designs/       # Screenshots, mood boards, design references
├── diary/         # Journal entries (any format)
└── thoughts/      # Brain dumps, ideas, notes
```

### The Wiki (`wiki/`)
LLM-generated markdown files. The LLM owns this layer entirely — creates pages, updates them, maintains cross-references, keeps everything consistent. The human reads it; the LLM writes it.

```
wiki/
├── _index.md            # Master catalog of all articles
├── _backlinks.json      # Reverse link graph
├── _absorb_log.json     # Tracks which raw entries have been absorbed
├── _tags.md             # Tag taxonomy
├── _type_index/         # Per-type structured JSON indices
│   ├── people.json
│   ├── music.json
│   ├── movies.json
│   ├── books.json
│   └── conversations.json
├── people/              # Person profiles
├── projects/            # Work, side projects, code
├── philosophies/        # Recurring beliefs, worldviews
├── patterns/            # Behavioral patterns, habits
├── eras/                # Life periods, transitions
├── music/               # Albums, artists, playlists, taste
├── movies/              # Films, shows, ratings
├── books/               # Books, reading journey
└── conversations/       # Thematic conversation articles
```

### The Schema (this file)
Tells the LLM how the wiki is structured, what conventions to follow, and what workflows to run. The human and LLM co-evolve this over time.

## Directory Taxonomy

Directories emerge from data. Don't pre-create empty categories — let them arise naturally. The above directories are starting points. New directories can be created when a clear category emerges (e.g., `tools/`, `places/`, `recipes/`).

| Directory | What belongs here |
|---|---|
| `people/` | One article per person. Unified profile across all sources. |
| `projects/` | Work projects, side projects, code repos, creative endeavors |
| `philosophies/` | Recurring beliefs, worldviews, guiding principles |
| `patterns/` | Behavioral patterns, habits, tendencies — things that repeat |
| `eras/` | Life periods, transitions, turning points |
| `music/` | Albums, artists, playlists, musical taste evolution |
| `movies/` | Films, shows, with personal ratings and reactions |
| `books/` | Books, reading notes, themes extracted |
| `conversations/` | Thematic articles synthesized from chat data — NOT per-chat dumps |

## Frontmatter Schemas

Every wiki article has YAML frontmatter. The schema depends on the article type.

### Person (`people/`)
```yaml
---
title: "Jane Doe"
type: person
created: 2026-04-06
last_updated: 2026-04-06
related: ["[[Career Doubts]]", "[[College Era]]"]
sources: [whatsapp_jane_dm, whatsapp_college_group, diary_2025_03]
aliases: ["Jane D", "Jane"]
context: "College friend, software engineer, frequent late-night philosophy conversations"
---
```

### Music (`music/`)
```yaml
---
title: "Discovery by Daft Punk"
type: music/album
rating: 9
artist: "Daft Punk"
genres: [electronic, french-house]
created: 2026-04-06
last_updated: 2026-04-06
related: ["[[French House]]", "[[2019 Summer]]"]
sources: [spotify_2019_03, diary_2019_03_15]
---
```

### Movie (`movies/`)
```yaml
---
title: "Blade Runner 2049"
type: movie
rating: 8.5
director: "Denis Villeneuve"
year: 2017
genres: [sci-fi, neo-noir]
created: 2026-04-06
last_updated: 2026-04-06
related: ["[[Sci-Fi Philosophy]]", "[[Visual Aesthetics]]"]
sources: [imdb_ratings, diary_2023_11]
---
```

### Book (`books/`)
```yaml
---
title: "Meditations by Marcus Aurelius"
type: book
rating: 9
author: "Marcus Aurelius"
status: completed
genres: [philosophy, stoicism]
created: 2026-04-06
last_updated: 2026-04-06
related: ["[[Stoicism]]", "[[Self-Discipline Pattern]]"]
sources: [goodreads_export, diary_2024_01]
---
```

### Conversation Theme (`conversations/`)
```yaml
---
title: "Late Night Philosophy with Jane"
type: conversation
people: ["[[Jane Doe]]"]
period: "2024-01 to 2025-06"
groups: [college_friends]
created: 2026-04-06
last_updated: 2026-04-06
related: ["[[Existentialism]]", "[[Career Doubts]]"]
sources: [whatsapp_jane_dm, whatsapp_college_group]
---
```

### Philosophy (`philosophies/`)
```yaml
---
title: "Build Things That Last"
type: philosophy
created: 2026-04-06
last_updated: 2026-04-06
related: ["[[Side Projects]]", "[[Engineering Patterns]]"]
sources: [diary_2024_06, whatsapp_jane_dm]
---
```

### Pattern (`patterns/`)
```yaml
---
title: "Late Night Productivity"
type: pattern
created: 2026-04-06
last_updated: 2026-04-06
related: ["[[Sleep Patterns]]", "[[Creative Work]]"]
sources: [diary_2024_q3, whatsapp_work_group]
---
```

### Era (`eras/`)
```yaml
---
title: "College Years (2018-2022)"
type: era
period: "2018-09 to 2022-06"
created: 2026-04-06
last_updated: 2026-04-06
related: ["[[Jane Doe]]", "[[Computer Science]]"]
sources: [diary_2018_to_2022, whatsapp_college_group]
---
```

### Project (`projects/`)
```yaml
---
title: "Personal Wiki"
type: project
status: active
created: 2026-04-06
last_updated: 2026-04-06
related: ["[[Knowledge Management]]", "[[LLM Tools]]"]
sources: [diary_2026_04]
---
```

## Absorption Rules

### The Absorption Loop
When processing raw entries into wiki articles:

1. Read the entry with full context.
2. Understand its meaning within the larger life narrative.
3. Match against existing articles using `_index.md`.
4. Update relevant articles, rewriting sections for coherence (don't just append).
5. Create new articles only when warranted by substantial material.
6. Identify emerging patterns that deserve concept articles.
7. Every 15 entries: checkpoint with quality audit.

### Anti-Patterns — DO NOT
- **Diary structure**: Section headings as dates instead of themes. Articles are thematic, not chronological.
- **Peacock language**: "legendary," "groundbreaking," "profound," "fascinating."
- **Mechanical filing**: Dropping facts without synthesis.
- **Editorial voice**: "Interestingly," "it should be noted," "remarkably."
- **Stub articles**: Creating pages with 3 lines. If there isn't enough material, enrich an existing article instead.
- **Cramming**: Shoving everything about a topic into one bloated page. Split when a section could stand alone.

### Quality Standards
- **Minimum viable article**: 15 lines of content (excluding frontmatter).
- **Target range**: 20-100 lines depending on significance.
- **Quote discipline**: Maximum 3 direct quotes per article. Let synthesis carry the weight.
- **Structure**: Thematic sections with clear headers. Not a list of bullet points.
- **Tone**: Encyclopedic. Flat, factual prose. Direct quotes carry emotional weight. Write as if documenting a life for someone who wants to understand it, not someone who lived it.

### The Concrete Noun Test
When absorbing an entry, extract named entities — people, places, companies, books, tools, albums. But only if they're referenced meaningfully, not in passing. Each meaningful entity should have or be part of a wiki article.

## Wikilinks

Use `[[Article Title]]` syntax to link between articles. The article title must match exactly (case-sensitive). When creating a new article, immediately add wikilinks to related existing articles and update those articles to link back.

## Index Maintenance

### `_index.md`
Master catalog of every article. Each entry: link, one-line summary, type. Organized by directory/category. Updated on every ingest/absorb operation. When answering a query, read this first to find relevant pages.

### `_backlinks.json`
Tracks which articles reference which other articles. Structure:
```json
{
  "Jane Doe": {
    "referenced_by": ["Late Night Philosophy with Jane", "College Years (2018-2022)"],
    "count": 2
  }
}
```
Rebuilt by scanning all `[[wikilinks]]` across articles.

### `_type_index/*.json`
Structured per-type indices with typed metadata for filtering/querying. Each entry mirrors the frontmatter of articles of that type. Enables queries like "all books rated 8+" or "all people from the college era."

### `_tags.md`
Flat taxonomy of all tags used across articles. Helps identify clustering and gaps.

### `_absorb_log.json`
Tracks which raw entries have been absorbed and when. Prevents double-processing. Structure:
```json
{
  "absorbed": [
    {"entry": "raw/whatsapp/college_friends.txt", "date": "2026-04-06", "articles_touched": 5}
  ]
}
```

## Person Identity Resolution

People appear under different names across sources. The `people_aliases.yaml` file at the project root maps all known aliases to a canonical identity.

### How it works:
1. When ingesting a new source, the LLM extracts all person names/identifiers.
2. The LLM matches against existing entries in `people_aliases.yaml`.
3. For unmatched names, the LLM proposes new entries or suggests merges.
4. The human reviews and confirms.
5. The confirmed mapping is used for all wiki operations — every reference to a person resolves to their canonical name and links to their `people/` article.

### Matching heuristics:
- Exact match on any alias
- Fuzzy match on name (e.g., "Jane" matches "Jane Doe" if context supports it)
- Phone number match (WhatsApp exports may use numbers instead of names)
- Context match (same group, same topics, same time period)

When uncertain, ask. Never silently merge two people.

## Querying the Wiki

When answering a question:
1. Read `_index.md` to identify relevant articles.
2. Read those articles.
3. If the answer requires cross-referencing, follow wikilinks to connected articles.
4. Synthesize an answer with citations to specific articles.
5. Assess the answer's wiki value and act immediately — do not just recommend:
   - **Worth keeping — new article**: Create a proper wiki article with correct frontmatter, wikilinks, encyclopedic tone. Update `_index.md`, `_backlinks.json`, and the relevant `_type_index/*.json`.
   - **Worth keeping — enrich existing**: Update existing article(s) with new material. Rewrite for coherence, do not append. Update `_backlinks.json` if new wikilinks were added.
   - **Ephemeral**: Show the answer only, make no wiki changes.

## Lint / Health Check

Periodically audit the wiki for:
- Contradictions between articles
- Stale claims superseded by newer sources
- Orphan articles with no inbound wikilinks
- Important concepts mentioned but lacking their own article
- Missing cross-references
- Broken wikilinks (referencing articles that don't exist)
- Articles below minimum quality (under 15 lines)
- Data gaps that could be filled with available sources
