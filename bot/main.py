from handlers.commands import *
from handlers.callbacks import *
from config import *


@logger.catch()
def main() -> None:
    logger.warning('Bot is running!')
    updater.start_polling()


if __name__ == '__main__':
    main()
