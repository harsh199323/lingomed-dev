# LingoMed

A Python-based tool for extracting and analyzing medical German text to generate language learning exercises. LingoMed crawls medical content from German Wikipedia and identifies sentences containing medical terminology and specific grammatical patterns (Passiv, Konjunktiv I, Relativsätze) to create targeted language learning materials.

## Features

- **Corpus Crawling**: Automatically fetches medical articles from German Wikipedia
- **Medical Term Detection**: Identifies sentences containing predefined medical vocabulary
- **Grammar Pattern Recognition**: Uses spaCy to detect specific German grammatical structures:
  - Passiv (Passive voice)
  - Konjunktiv I (Subjunctive I)
  - Relativsätze (Relative clauses)
- **Exercise Generation**: Creates language learning exercises based on detected patterns
- **YAML Output**: Exports results in structured YAML format for easy processing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd lingomed
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Download the German spaCy model:
```bash
python -m spacy download de_core_news_sm
```

## Project Structure

```
lingomed/
├── config/
│   └── pattern.yml          # Medical terms and grammar patterns configuration
├── src/
│   ├── __init__.py
│   ├── corpus_crawler.py     # Wikipedia crawling functionality
│   ├── sentence_extractor.py # Text analysis and pattern matching
│   └── main.py              # Main execution script
├── tests/
│   ├── __init__.py
│   └── test_sentence_extractor.py
├── data/
│   └── corpora/             # Downloaded corpus files (created at runtime)
├── results/                 # Output files (created at runtime)
├── requirements.txt
└── README.md
```

## Usage

### Basic Usage

Run the main script to crawl Wikipedia medical articles and extract exercises:

```bash
python src/main.py
```

This will:
1. Fetch medical articles from German Wikipedia
2. Combine all corpus files
3. Extract sentences with medical terms and grammar patterns
4. Generate exercise suggestions
5. Save results to `results/extracted_exercises.yml`

### Configuration

Edit `config/pattern.yml` to customize:

- **Medical terms**: Add or modify the list of medical vocabulary to detect
- **Grammar patterns**: Modify spaCy pattern rules for grammatical structures

Example configuration:
```yaml
medical_terms:
  - Infektion
  - Pflege
  - Anamnese
  - Diagnose
  # ... more terms

grammar_patterns:
  Passiv:
    - {TAG: "VAFIN"}
    - {OP: "*", IS_PUNCT: false}
    - {TAG: "VVPP"}
  # ... more patterns
```

### Direct Usage of Components

#### Corpus Crawler
```python
from src.corpus_crawler import CorpusCrawler

crawler = CorpusCrawler()
wiki_file = crawler.fetch_wikipedia_medical(
    categories=["Medizin", "Krankheit", "Diagnostik"],
    max_articles=50
)
```

#### Sentence Extractor
```python
from src.sentence_extractor import SentenceExtractor

extractor = SentenceExtractor()
results = extractor.extract_sentences(
    corpus_path="path/to/corpus.txt",
    output_path="results/exercises.yml",
    max_sentences=100
)
```

## Output Format

The tool generates YAML files with the following structure:

```yaml
- sentence: "Die Diagnose wurde vom Arzt gestellt."
  medical_terms: ["Diagnose", "Arzt"]
  grammar: "Passiv"
  matched_pattern: "wurde gestellt"
  exercise_suggestion: "Convert to active voice: 'Die Diagnose wurde vom Arzt gestellt.' (Focus on term: Diagnose)"

- sentence: "Der Patient, dessen Anamnese sorgfältig erhoben wurde, zeigte Verbesserung."
  medical_terms: ["Patient", "Anamnese"]
  grammar: "Relativsatz"
  matched_pattern: "dessen erhoben"
  exercise_suggestion: "Split into two simple sentences: '...' (Focus on term: Patient)"
```

## Testing

Run the test suite:

```bash
pytest tests/
```

Or run specific tests:
```bash
pytest tests/test_sentence_extractor.py -v
```

## Dependencies

- **spacy**: NLP processing and pattern matching
- **stanza**: Alternative NLP library (future use)
- **pyyaml**: YAML file processing
- **tqdm**: Progress bars
- **pytest**: Testing framework
- **Wikipedia-API**: Wikipedia content fetching
- **beautifulsoup4**: HTML parsing
- **requests**: HTTP requests

## Language Model Requirements

This project requires the German spaCy model:
```bash
python -m spacy download de_core_news_sm
```

## Configuration Options

### Medical Terms
The `medical_terms` list in `config/pattern.yml` contains German medical vocabulary. Add terms relevant to your specific domain or learning objectives.

### Grammar Patterns
Grammar patterns use spaCy's pattern matching syntax. Each pattern is a list of token specifications that define the grammatical structure to match.

## Error Handling

The application includes comprehensive error handling and logging:
- File not found errors for missing corpus or configuration files
- Import errors for missing dependencies
- Processing errors during text analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

[Add your license information here]

## Troubleshooting

### Common Issues

1. **Missing spaCy model**: Install with `python -m spacy download de_core_news_sm`
2. **Configuration file not found**: Ensure `config/pattern.yml` exists in the project root
3. **Wikipedia API errors**: Check internet connection and API rate limits
4. **Memory issues**: Reduce `max_articles` or `max_sentences` parameters

### Performance Tips

- Start with smaller `max_articles` values for testing
- Use `max_sentences` to limit output size
- Monitor memory usage with large corpora

## Future Enhancements

- Support for additional languages
- Integration with learning management systems
- Web interface for interactive exercise creation
- Machine learning-based difficulty assessment
- Export to various formats (JSON, CSV, etc.)

## Contact

[Add your contact information here]