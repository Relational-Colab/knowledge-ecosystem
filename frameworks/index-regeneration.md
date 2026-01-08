# Index Regeneration Framework

## Purpose
Define the conceptual workflow for automatically regenerating multilingual lookup indexes (e.g., index-en-zh.yaml) from individual term files.

## Inputs
- i18n/schema.yaml
- i18n/en/*.yaml
- i18n/zh/*.yaml
- (future languages)

## Outputs
- i18n/index-en-zh.yaml
- (future language-pair indexes)

## Workflow Overview
1. Scan the i18n/en/ directory for term files.
2. For each ID, locate the corresponding file in the target language directory.
3. Extract fields: term, pronunciation, topic, tags.
4. Assemble entries into a sorted list.
5. Write the output to the appropriate index file.

## Sorting Options
- By English term
- By Chinese characters
- By pinyin
- By topic
- By ID

## Future Automation Hooks
- Pre-commit hooks
- GitHub Actions
- Teaching material generation
- Flashcard generation
- Topic-based glossaries

## Governance Notes
- Keep automation optional and transparent.
- Maintain human readability of index files.
- Ensure scripts respect schema.yaml.
