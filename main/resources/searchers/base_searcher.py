

class BaseSearcher(object):
    def __init__(self, base_url, phrases, searcher_conf=None):
        self.base_url = base_url
        self.search_phrases = phrases
        self.searcher_conf = searcher_conf

    def start_search(self, *args, **kwargs):
        pass

    def create_item(self, *args, **kwargs):
        pass
