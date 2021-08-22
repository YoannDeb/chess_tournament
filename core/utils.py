"""
Module for MenuData class, used by controllers and views.
"""


class MenuData:
    """
    A class creating objects that stores the data of a menu.
    Typically created by a controller and send to a view.
    """
    def __init__(self):
        """
        Initiates all types of data and a counter:
        - self.lines: A list of the lines that will be printed in the menu.
        - self.entries: A dictionary storing an entry that can be choose by the user.
        - self.input_message: A message that will be printed at the input of an "Entry" menu.
        - self.queries : A list of queries that necessitate data from the user.
        - self.autokey: A counter for automatically numerated entries.
        """
        self.lines = []
        self.entries = {}
        self.input_message = None
        self.queries = []
        self.autokey = 1

    def add_line(self, text):
        """
        Adds a line to the self.lines list.
        :param text: A string that will be printed in the menu.
        """
        self.lines.append(text)

    def add_entry(self, key, menu_option, response):
        """
        Add an entry to the self.entries dictionary.
        :param key: Dictionary key, that will be the input the user will enter if he choses this one.
                    If auto, it will be auto-assigned. "top_menu" will be the last attribute.
                    Else "bottom-menu" will be the last_attribute.
                    Permits to separate the auto-assigned of the specific entries in the menu.
                    Specific entries are often important entries and needs to be separated in the menu for clarity.
        :param menu_option: Description string of the entry shown to the user.
        :param response: Will be the response of the entry if chosen, returned by get_user_choice().
                         The response can be a string, an object...
        """
        if key == "auto":
            key = self.autokey
            self.autokey += 1
            self.entries[str(key)] = (menu_option, response, "top_menu")
        else:
            self.entries[str(key)] = (menu_option, response, "bottom_menu")

    def add_input_message(self, text):
        """
        A message that will be printed at the input of an "Entry" menu.
        :param text: A string for the input that will be showed in the view.
        """
        self.input_message = text

    def add_query(self, text):
        """
        Adds a query in self.queries list.
        :param text: A string for the input that will be showed in the view.
        """
        self.queries.append(text)

    def clear_data(self):
        """
        Reinitialise all attributes of a MenuData instance.
        """
        self.entries = {}
        self.lines = []
        self.queries = []
        self.input_message = None
        self.autokey = 1
