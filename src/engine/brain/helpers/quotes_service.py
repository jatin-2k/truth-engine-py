from src.models.quote import QuoteModel
from typing import List, Dict
from pydantic import TypeAdapter

class QuotesManager:
    def __init__(self, quotes_file_path: str):
        self.quotes_file_path = quotes_file_path
        self.adapter = TypeAdapter(Dict[str, List[QuoteModel]])

    def get_quotes(self, item_id: str) -> List[QuoteModel]:
        quotes = []
        with open(self.quotes_file_path, 'r') as f:
            file_content = f.read()
            if file_content:
                quotes_registry = self.adapter.validate_json(file_content)
                if item_id in quotes_registry:
                    quotes = quotes_registry[item_id]
        return quotes
    
    def add_quote(self, quote: QuoteModel) -> None:
        quotes_registry = {}
        with open(self.quotes_file_path, 'r') as f:
            file_content = f.read()
            if file_content:
                quotes_registry = self.adapter.validate_json(file_content)
        
        if quote.item_id not in quotes_registry:
            quotes_registry[quote.item_id] = []
        
        if(quote.event_id not in [q.event_id for q in quotes_registry[quote.item_id]]):
            quotes_registry[quote.item_id].append(quote)
            quotes_registry[quote.item_id].sort(key=lambda q: q.timestamp, reverse=True)

        with open(self.quotes_file_path, 'wb') as f:
            f.write(self.adapter.dump_json(quotes_registry, indent=2))