# /wiki — Personal Wiki Operations

Operate on the personal wiki at this project root. All operations follow the conventions in `CLAUDE.md`.

## Usage

`/wiki <command> [args]`

## Commands

### `/wiki ingest <source-type> [path]`

Convert raw source files into normalized markdown entries in `raw/entries/`.

**Source types and their parsers:**

**whatsapp** — Parse WhatsApp `.txt` exports from `raw/whatsapp/`.
- Format: `[date, time] sender: message` (or `date, time - sender: message` depending on locale)
- Auto-detect group vs. 1-on-1 conversations
- Extract all participants
- Split into per-conversation entry files
- Handle multi-line messages, media placeholders (`<Media omitted>`), system messages
- Run person identity resolution against `people_aliases.yaml`
- Output: one `.md` entry file per conversation per date chunk

**spotify** — Parse Spotify data from `raw/spotify/`.
- Extended streaming history JSON or playlist exports
- Extract: track, artist, album, play duration, timestamp
- Group by meaningful periods (not individual plays)

**imdb** — Parse IMDB ratings CSV from `raw/imdb/`.
- Extract: title, year, rating, date rated, genres, directors

**goodreads** — Parse Goodreads CSV from `raw/goodreads/`.
- Extract: title, author, rating, date read, shelves, review

**designs** — Process design files from `raw/designs/`.
- Read images (screenshots, mood boards)
- Extract visual themes, patterns, color palettes
- Create entry with image references

**diary** — Parse journal entries from `raw/diary/`.
- Support: plain text, markdown, Day One JSON
- Extract date, content, tags, mood (if present)

**thoughts** — Parse brain dumps from `raw/thoughts/`.
- Treat each file as one entry
- Extract date from filename or content

**generic** — Fallback for any text/markdown/CSV file.

**Ingest workflow:**
1. Read the raw source files
2. Parse according to source type
3. Generate normalized `.md` entry files with frontmatter (id, date, source_type, tags)
4. Update `_absorb_log.json` to record what was ingested
5. Report: number of entries created, participants found, date range covered

---

### `/wiki absorb [date-range]`

Compile raw entries into thematic wiki articles. This is the core operation.

**Date range options:**
- `all` — absorb everything not yet absorbed
- `last 30 days` — entries from the last 30 days
- `2026-03` — specific month
- `2026-03-15` — specific date
- No argument defaults to `all`

**Absorption workflow:**
1. Read `_absorb_log.json` to find unabsorbed entries
2. Read `_index.md` to know what articles exist
3. Read `people_aliases.yaml` for person resolution
4. For each entry:
   a. Read with full context
   b. Understand meaning within the larger narrative
   c. Match against existing articles
   d. Update relevant articles (rewrite for coherence, don't just append)
   e. Create new articles only when substantial material warrants it
   f. Identify emerging patterns → concept articles
5. Every 15 entries: checkpoint — audit quality, check for anti-patterns
6. After all entries: rebuild `_index.md`, `_backlinks.json`, type indices
7. Report: articles created, articles updated, patterns identified

**Critical rules during absorption:**
- Follow ALL rules in CLAUDE.md — especially anti-patterns and quality standards
- Articles are THEMATIC, not chronological
- Minimum 15 lines per article
- Max 3 quotes per article
- Encyclopedic tone
- Use `[[wikilinks]]` for every cross-reference

---

### `/wiki query <question>`

Answer a question by navigating the wiki. Automatically files worthy answers as wiki articles.

**Workflow:**
1. Read `_index.md` to identify relevant articles
2. Read those articles
3. Follow wikilinks to connected articles if needed
4. Synthesize answer with citations: `(see [[Article Name]])`
5. Assess the answer's wiki value and act immediately — do not just recommend:
   - **Worth keeping — new article**: Create a proper wiki article with correct frontmatter (type, title, related, sources), wikilinks throughout, and encyclopedic tone. Update `_index.md`, `_backlinks.json`, and the relevant `_type_index/*.json`. Report: "Filed as [[Article Title]] → `wiki/<dir>/`".
   - **Worth keeping — enrich existing**: Update the relevant existing article(s) with the new material — rewrite for coherence, do not append. Update `_backlinks.json` if new wikilinks were added. Report: "Enriched [[Article Title]]".
   - **Ephemeral**: The answer is useful now but adds no lasting wiki value. Show the answer only, make no wiki changes. Report: "Ephemeral — no wiki changes."

**Example queries:**
- "What do I know about Ahmed?"
- "What music was I listening to in 2023?"
- "What are my recurring career concerns?"
- "Who do I discuss philosophy with most?"

---

### `/wiki cleanup`

Audit and enrich the wiki. Run parallel checks:

1. **Structure audit**: orphan articles, broken wikilinks, missing backlinks
2. **Tone audit**: peacock language, editorial voice, diary-style sections
3. **Completeness audit**: articles under 15 lines, missing frontmatter fields
4. **Gap analysis**: concepts mentioned but lacking articles, people referenced but no profile
5. **Index rebuild**: regenerate `_index.md`, `_backlinks.json`, type indices

Report all findings. Fix automatically where safe (broken links, missing index entries). Ask before making substantive content changes.

---

### `/wiki breakdown`

Identify and create missing articles.

1. Scan all existing articles for `[[wikilinks]]` that point to non-existent articles
2. Scan for recurring themes, people, or concepts that deserve their own page
3. Check type indices for gaps (e.g., person mentioned in 5 articles but has no profile)
4. Propose a list of articles to create, with justification
5. On confirmation, create them

Use `--reorganize` flag to also restructure the wiki hierarchy (move articles between directories, split bloated articles, merge thin ones).

---

### `/wiki rebuild-index`

Rebuild all index and metadata files from scratch by scanning the wiki:

1. Scan all `.md` files in `wiki/`
2. Rebuild `_index.md` from frontmatter
3. Rebuild `_backlinks.json` from `[[wikilinks]]`
4. Rebuild all `_type_index/*.json` from frontmatter
5. Rebuild `_tags.md` from all tags
6. Report: total articles, articles per type, orphans, most-connected pages

---

### `/wiki resolve-people`

Run person identity resolution across all sources.

1. Scan all raw entries and wiki articles for person names/identifiers
2. Match against `people_aliases.yaml`
3. Cluster unmatched names using fuzzy matching + context
4. Present proposed matches/merges to user for confirmation
5. Update `people_aliases.yaml` with confirmed mappings
6. Update wiki articles to use canonical names
7. Rebuild people type index

---

### `/wiki status`

Display wiki statistics:

- Total articles by type
- Total raw entries (absorbed vs. pending)
- Most recently updated articles
- Orphan articles (no inbound links)
- Most connected articles (highest backlink count)
- People profiles count vs. unique names in sources
- Pending absorption count
