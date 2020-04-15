from datetime import datetime

class Entry():
    def __init__(self, entry_dict):
        super().__init__()
        self.id = entry_dict['item_id']
        self.title = entry_dict['resolved_title']
        self.url = entry_dict['resolved_url']
        self.updated = datetime.utcfromtimestamp(int(entry_dict['time_updated']))
        self.added = datetime.utcfromtimestamp(int(entry_dict['time_added']))

    @staticmethod
    def parse_list(xs):
        return list(map(lambda x: Entry(x), xs))

    def __str__(self):
        return f"{self.id}\n{self.title}\n{self.url}\nAdded:{self.added} - Updated: {self.updated}"
