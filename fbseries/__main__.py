try:
    from fbseries.controller import Controller
except ImportError:
    from .controller import Controller


def main():
    app = Controller()
    app.run()


if __name__ == '__main__':
    main()
