import pytest
import os
from src.sentence_extractor import SentenceExtractor
import yaml

@pytest.fixture
def test_data_dir(tmp_path):
    return tmp_path

@pytest.fixture
def config_dir(test_data_dir):
    config_dir = os.path.join(test_data_dir, "config")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

@pytest.fixture
def sample_config(config_dir):
    config = {
        "medical_terms": ["Diagnose", "Patient", "Therapie", "Symptom", "Anamnese"],
        "grammar_patterns": {
            "Passiv": [{"TAG": "VAFIN", "DEP": "aux"}, {"TAG": "VVPP"}],
            "Konjunktiv_I": [{"TAG": "VMFIN", "MORPH": {"REGEX": "Mood=Sub"}}],
            "Relativsatz": [{"POS": "PRON", "DEP": "rel"}, {"POS": "VERB"}]
        }
    }
    config_path = os.path.join(config_dir, "pattern.yml")
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True)
    return config_path

@pytest.fixture
def sample_corpus(test_data_dir):
    corpus = """
Die Diagnose wurde vom Arzt gestellt.
Der Patient berichtet über starke Symptome.
Es sei darauf hingewiesen, dass die Therapie erfolgreich verlief.
Der Patient, dessen Anamnese sorgfältig erhoben wurde, zeigte Verbesserung.
"""
    corpus_path = os.path.join(test_data_dir, "test_corpus.txt")
    with open(corpus_path, "w", encoding="utf-8") as f:
        f.write(corpus)
    return corpus_path

@pytest.fixture
def output_path(test_data_dir):
    return os.path.join(test_data_dir, "results", "test_output.yml")

def test_extraction(sample_config, sample_corpus, output_path):
    extractor = SentenceExtractor()
    results = extractor.extract_sentences(
        corpus_path=sample_corpus,
        output_path=output_path,
        max_sentences=3
    )
    
    assert len(results) > 0
    # Check first result contains medical term and grammar pattern
    assert any(result["medical_terms"] for result in results)
    assert all("grammar" in result for result in results)
    
    # Verify output file was created
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        saved_results = yaml.safe_load(f)
    assert len(saved_results) == len(results)