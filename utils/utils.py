class MenuData:
    def __init__(self):
        self.entries = {}
        self.headers = []
        self.queries = []
        self.input_message = None
        self.autokey = 1

    def add_entry(self, key, menu_option, destination_controller):
        if key == "auto":
            key = self.autokey
            self.autokey += 1

        self.entries[str(key)] = (menu_option, destination_controller)

    def add_header(self, text):
        self.headers.append(text)

    def add_query(self, text):
        self.queries.append(text)

    def add_input_message(self, text):
        self.input_message = text

    def clear_data(self):
        self.entries = {}
        self.headers = []
        self.queries = []
        self.input_message = None
        self.autokey = 1

    def add_row(self):
        pass