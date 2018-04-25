"""Main module of fbseries."""

from fbseries.controller import Controller


def main():
    """Run app."""
    app = Controller()
    app.run()


if __name__ == '__main__':
    main()
