from multiprocessing.pool import ThreadPool


class BaseSearcher(object):
    def __init__(self, base_url, phrases, searcher_name, searcher_conf=None):
        self.base_url = base_url
        self.search_phrases = phrases
        self.searcher_conf = searcher_conf
        self.searcher_name = searcher_name
        self.all_results = []

    def start_search(self, *args, **kwargs):
        pass

    def create_item(self, *args, **kwargs):
        pass

    def do_the_job(self, job, args=None):
        if args:
            job(*args)
        else:
            job()

    def return_results(self, custom_modifier=None):
        if custom_modifier and callable(custom_modifier):
            return self.searcher_name, custom_modifier(self.all_results)
        else:
            return self.searcher_name, self.all_results


class ThreadedSearcher(BaseSearcher):
    def __init__(self, base_url, phrases, searcher_name, searcher_conf=None):
        super(ThreadedSearcher, self).__init__(base_url, phrases, searcher_name, searcher_conf)
        process_count = min(len(phrases) or 1, 10)
        self.thread_pool = ThreadPool(processes=process_count)

    def do_the_job(self, job, args=None):
        if args:
            self.thread_pool.apply_async(job, args=args, callback=self.search_callback)
        else:
            self.thread_pool.apply_async(job, callback=self.search_callback)

    def return_results(self, custom_modifier=None):
        self.thread_pool.close()
        self.thread_pool.join()
        return super(ThreadedSearcher, self).return_results(custom_modifier)

    def search_callback(self, result):
        self.all_results.extend(result)
