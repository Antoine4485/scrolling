# README : FICHIER A EXECUTER DIRECTEMENT DANS L'INVITE DE COMMANDE WINDOWS
# SCROLLING HORIZONTAL ET VERTICAL OK
# COULEURS OK

import curses
import yaml


class Scrolling:

    def __init__(self, scrolling_type="horizontal"):
        self.scrolling_type = scrolling_type
        self.config = self._get_config()
        self.screen = curses.initscr()
        self.show_in_command_line()

    @staticmethod
    def _get_config():
        with open("config.yml", 'r', encoding='utf8') as file:
            config = {}
            try:
                # Chargement du fichiers
                config = yaml.safe_load(file)
            except yaml.YAMLError as ex:
                print("YAML FILE HAS SYNTAX ERROR :")
                print(ex)
            finally:
                return config

    def show_text(self, text_to_show, sign):
        scroll_text_padding, sep = (" ", "|") if self.scrolling_type == "horizontal" else ("", "-")
        draw = f"{sep}{self.config["text"]["fixed"]:^{self.config["scrolling"][self.scrolling_type]["fixed_text"]}}" \
               f"{sep}{scroll_text_padding}{text_to_show:{sign}{self.config["scrolling"][self.scrolling_type]["length"]}}" \
               f"{scroll_text_padding}{sep}"
        position = self.config["scrolling"][self.scrolling_type]["position"]

        for i, letter in enumerate(draw):
            if self.scrolling_type == "vertical":
                self.screen.addstr(position[1] + i, position[0], letter)
            else:
                self.screen.addstr(position[1], position[0] + i, letter)

        self.screen.refresh()
        curses.delay_output(round(100000 / self.config["scrolling"][self.scrolling_type]["speed"]))

    def show_in_command_line(self):
        if not self.config:
            return

        curses.start_color()
        text = self.config["text"]["scroll"]
        length = self.config["scrolling"][self.scrolling_type]["length"]
        cpt = 0

        while True and cpt < 2:
            cpt += 1

            if self.config["scrolling"][self.scrolling_type]["direction"] in ("up", "left"):
                start = 0
                for i in range(len(text) + length):
                    if i >= length:
                        start += 1
                    sign = ">"
                    if i >= len(text):
                        sign = "<"
                    self.show_text(text[start:i + 1], sign)
            else:
                for i in range(len(text), -length, -1):
                    start = i
                    sign = "<"
                    if start < 0:
                        start = 0
                        sign = ">"
                    self.show_text(text[start:i + length], sign)

        self.screen.getch()
        curses.endwin()


if __name__ == '__main__':

    Scrolling("vertical")
    #Scrolling()