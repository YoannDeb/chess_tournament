class Menu:
    def __init__(self):
        self.entries = {}
        self.autokey = 1

    def add(self, key, menu_option, destination_controller):
        if key == "auto":
            key = self.autokey
            self.autokey += 1

        self.entries[key] = (menu_option, destination_controller)

# menu = Menu()
# menu.add("auto", "première option", lambda: None)
# menu.add("auto", "première option", lambda: None)
# menu.add("auto", "première option", lambda: None)
# menu.add("auto", "première option", lambda: None)
# menu.add("q", "quitter", lambda: None)
# menu.add(6, "sixième option", lambda: None)
# print(menu.entries)

