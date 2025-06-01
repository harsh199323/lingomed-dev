from corpus_crawler import CorpusCrawler
from sentence_extractor import SentenceExtractor
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize crawlers and extractors
        logger.info("Initializing corpus crawler...")
        crawler = CorpusCrawler()
        
        logger.info("Initializing sentence extractor...")
        extractor = SentenceExtractor()
        
        # Set up paths
        base_dir = os.path.dirname(os.path.dirname(__file__))
        output_path = os.path.join(base_dir, "results", "extracted_exercises.yml")
        
        # Fetch corpus data
        logger.info("Fetching medical texts from Wikipedia DE...")
        wiki_corpus = crawler.fetch_wikipedia_medical(
            categories=["Medizin", "Krankheit", "Diagnostik"],
            max_articles=20  # Start with fewer articles for testing
        )
        
        logger.info("Combining corpora...")
        combined_corpus = crawler.combine_corpora()
        
        # Extract sentences
        logger.info("Extracting exercises...")
        results = extractor.extract_sentences(
            corpus_path=combined_corpus,
            output_path=output_path,
            max_sentences=150
        )
        
        logger.info(f"Successfully extracted {len(results)} exercises to {output_path}")
        
    except ImportError as e:
        logger.error(f"Import error: {str(e)}. Make sure all required packages are installed.")
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")

if __name__ == "__main__":
    main()