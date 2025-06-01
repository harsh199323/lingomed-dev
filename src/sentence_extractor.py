import spacy
from spacy.matcher import Matcher
import yaml
from tqdm import tqdm
import os

class SentenceExtractor:
    def __init__(self):
        # Load spaCy NLP engine
        self.nlp = spacy.load("de_core_news_sm")
        
        # Load patterns from config
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "pattern.yml")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                self.medical_terms = config["medical_terms"]
                self.grammar_patterns = config["grammar_patterns"]
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
        
        # Initialize matcher with proper pattern lists
        self.matcher = Matcher(self.nlp.vocab)
        for grammar_type, pattern in self.grammar_patterns.items():
            # Convert pattern list to proper format expected by matcher
            pattern_list = []
            for token in pattern:
                pattern_list.append(token)
            self.matcher.add(grammar_type, [pattern_list])

    def extract_sentences(self, corpus_path, output_path, max_sentences=150):
        if not os.path.exists(corpus_path):
            raise FileNotFoundError(f"Corpus file not found at {corpus_path}")

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Read corpus
        with open(corpus_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Process with SpaCy
        doc = self.nlp(text)
        
        # Process with SpaCy in batches
        batch_size = 1000
        results = []
        
        print("Analyzing sentences for medical terms and grammar patterns...")
        sentences = list(doc.sents)
        
        for i in tqdm(range(0, len(sentences), batch_size), desc="Processing batches"):
            batch = sentences[i:i + batch_size]
            
            for sent in batch:
                # Medical term check
                medical_found = [term for term in self.medical_terms if term.lower() in sent.text.lower()]
                if not medical_found:
                    continue
                
                # Grammar check
                sent_doc = self.nlp(sent.text)
                matches = self.matcher(sent_doc)
                
                if matches:
                    match_id, start, end = matches[0]
                    grammar_type = self.nlp.vocab.strings[match_id]
                    pattern_tokens = [sent_doc[i].text for i in range(start, end)]
                    
                    result = {
                        "sentence": sent.text.strip(),
                        "medical_terms": medical_found,
                        "grammar": grammar_type,
                        "matched_pattern": " ".join(pattern_tokens),
                        "exercise_suggestion": self._generate_exercise_suggestion(
                            sent.text.strip(), 
                            medical_found[0], 
                            grammar_type
                        )
                    }
                    results.append(result)
                    
                    if len(results) >= max_sentences:
                        break
            
            if len(results) >= max_sentences:
                break
        
        # Save results
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(results, f, allow_unicode=True)
        
        return results

    def _generate_exercise_suggestion(self, sentence, medical_term, grammar_type):
        """Generate exercise suggestions based on the type of match"""
        if grammar_type == "Passiv":
            return f"Convert to active voice: '{sentence}' (Focus on term: {medical_term})"
        elif grammar_type == "Konjunktiv_I":
            return f"Convert to indicative mood: '{sentence}' (Focus on term: {medical_term})"
        elif grammar_type == "Relativsatz":
            return f"Split into two simple sentences: '{sentence}' (Focus on term: {medical_term})"
        return f"Gap-fill for [{medical_term}] OR [{grammar_type}] structure"

if __name__ == "__main__":
    extractor = SentenceExtractor()
    base_dir = os.path.dirname(os.path.dirname(__file__))
    corpus_path = os.path.join(base_dir, "data", "corpus.txt")
    output_path = os.path.join(base_dir, "results", "extracted_sentences.yml")
    
    try:
        results = extractor.extract_sentences(
            corpus_path=corpus_path,
            output_path=output_path,
            max_sentences=200
        )
        print(f"Successfully extracted {len(results)} sentences to {output_path}")
    except Exception as e:
        print(f"Error during extraction: {str(e)}")