import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from views.IntroView import IntroView


def main():
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
    menu_view = IntroView(window)
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
