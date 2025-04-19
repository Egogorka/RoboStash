import logging

def set_basic_config() -> None:
    print("start logging")
    logging.basicConfig(level=logging.INFO, filename="./Logging_info/logging_info.log", filemode='w',
                        format="%(asctime)s %(levelname)s %(message)s"
                        )


