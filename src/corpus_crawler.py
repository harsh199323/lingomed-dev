import requests
from bs4 import BeautifulSoup
import wikipediaapi
from tqdm import tqdm
import os

class CorpusCrawler:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.corpus_dir = os.path.join(self.base_dir, "data", "corpora")
        os.makedirs(self.corpus_dir, exist_ok=True)
        
        # Set up Wikipedia API with German language
        self.wiki = wikipediaapi.Wikipedia(
            language='de',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='LingoMed/1.0'
        )

    def fetch_wikipedia_medical(self, categories=["Medizin", "Krankheit", "Diagnostik"], max_articles=50):
        """Fetch medical articles from German Wikipedia"""
        output_file = os.path.join(self.corpus_dir, "wiki_medical.txt")
        
        articles = []
        for category in tqdm(categories, desc="Fetching categories"):
            try:
                cat_page = self.wiki.page(f"Category:{category}")
                if cat_page.exists():
                    # Get category members
                    members = list(cat_page.categorymembers.values())[:max_articles//len(categories)]
                    for page in members:
                        if page.exists() and not page.title.startswith('Category:'):
                            articles.append(page.text)
            except Exception as e:
                print(f"Error processing category {category}: {str(e)}")
                continue

        # Save to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n\n".join(articles))
        
        return output_file

    def combine_corpora(self):
        """Combine all corpus files into one"""
        combined_file = os.path.join(self.corpus_dir, "combined_corpus.txt")
        corpus_files = [f for f in os.listdir(self.corpus_dir) if f.endswith('.txt')]
        
        with open(combined_file, "w", encoding="utf-8") as f:
            for fname in corpus_files:
                with open(os.path.join(self.corpus_dir, fname), encoding="utf-8") as infile:
                    f.write(infile.read() + "\n\n")
        
        return combined_file