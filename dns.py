from src.modules.Router import Router
from src.modules.ArgParser import ArgParser


def main():
    parser = ArgParser()
    args = parser.parse_args()
    print(args)
    try:
        router = Router(args.ip, args.port)
        router.start()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')


if __name__ == '__main__':
    main()
