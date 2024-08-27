import curses
import yaml


class Scrolling:

    def __init__(self, scrolling_type="horizontal"):
        self.__scrolling_type = scrolling_type
        self.__config = self.__get_config()
        self.__screen = curses.initscr()
        self.__show_in_command_line()

    @staticmethod
    def __get_config():
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

    def __show_text(self, text_to_show, sign):
        scroll_text_padding, sep = (" ", "|") if self.__scrolling_type == "horizontal" else ("", "-")

        draw = f"{sep}{self.__config["text"]["fixed"]:^{self.__config["scrolling"][self.__scrolling_type]["fixed_text"]}}" \
               f"{sep}{scroll_text_padding}{text_to_show:{sign}{self.__config["scrolling"][self.__scrolling_type]["length"]}}" \
               f"{scroll_text_padding}{sep}"

        position = self.__config["scrolling"][self.__scrolling_type]["position"]

        for i, letter in enumerate(draw):
            if self.__scrolling_type == "vertical":
                self.__screen.addstr(position[1] + i, position[0], letter)
            else:
                self.__screen.addstr(position[1], position[0] + i, letter)

        self.__screen.refresh()
        curses.delay_output(round(100000 / self.__config["scrolling"][self.__scrolling_type]["speed"]))

    def __show_in_command_line(self):
        if not self.__config:
            return

        curses.start_color()
        text = self.__config["text"]["scroll"]
        length = self.__config["scrolling"][self.__scrolling_type]["length"]

        while True:

            if self.__config["scrolling"][self.__scrolling_type]["direction"] in ("up", "left"):
                start = 0
                for i in range(len(text) + length):
                    if i >= length:
                        start += 1
                    sign = ">"
                    if i >= len(text):
                        sign = "<"
                    self.__show_text(text[start:i + 1], sign)
            else:
                for i in range(len(text), -length, -1):
                    start = i
                    sign = "<"
                    if start < 0:
                        start = 0
                        sign = ">"
                    self.__show_text(text[start:i + length], sign)


if __name__ == '__main__':

    Scrolling("vertical")
    #Scrolling()