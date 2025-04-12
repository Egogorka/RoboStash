import re
from user_agents import parse


def open_logfile(path: str) -> str:
    """The function is designed to open a log file at a given path.
    It takes the path to the object as input and returns the contents of this file in string format.
    """
    try:
        with open(path, 'r') as logs:
            text = logs.read()
            return text
    except FileNotFoundError as e:
        print(str(e))


def get_all_logs(file: str) -> list[tuple]:
    f"""The function takes a string as input and returns a list of tuples with the following elements:\n
        tuple[0] — The IP address of the client that sent the request to the server\n
        tuple[1] — The remote name of the user making the request\n
        tuple[2] — ID of the user making the request\n
        tuple[3] — Date of request\n
        tuple[4] — Request time\n
        tuple[5] — UTC time zone\n
        tuple[6] — Request type: (GET, POST, PUT, DELETE) that the server received\n
        tuple[7] — The API of the website the request pertains to\n
        tuple[8] — The protocol used to connect to the server and its version\n
        tuple[9] — The status code that the server returned for the request\n
        tuple[10] — The amount of data in bytes sent back to the client\n
        tuple[11] — Sources from which the user was directed to the current website (referrer)\n
        tuple[12] — User agent string (UA-string), contains information about the browser and host device\n
        tuple[13] — The response time it took for the server to serve the request\n
        """
    reg_ex = re.compile(r"(\b(?:\d{1,3}\.){3}\d{1,3}\b) (\w+|\W) (\w+|\W) "
                        r"\[(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\+\d+)] "
                        r"\"(GET|POST|PUT|DELETE) ([/\w+]+) ([\w/.]+)\" "
                        r"(\d+) (\d+) \"(.+)\" \"(.+)\" (\d+)"
                        )
    try:
        logs_list = re.findall(reg_ex, file)
    except TypeError as e:
        print(e)
    else:
        return logs_list

def get_ua_list(logs: list[tuple]) -> list:
    """The function takes the processed log file as input and returns from it a list of UA-strings containing information about the user."""
    ua_list = []
    for i in range(len(logs)):
        ua_list.append(logs[i][-2])
    return ua_list

def ua_parser(ua_list: list) -> list[tuple]:
    f"""The function takes a list of ua-strings as input and returns a list of tuples containing information about the user.\n
        0 — device type\n
        1 — device brand\n
        2 — device model\n
        3 — operating system\n
        4 — OS version\n
        5 — browser type\n
        6 — browser version\n"""
    parsed_ua_list = []
    for ua in ua_list:
        parsed_ua = parse(ua)

        if parsed_ua.is_bot:
            device_type = "bot"
        elif parsed_ua.is_mobile:
            device_type = "mobile"
        elif parsed_ua.is_tablet:
            device_type = "tablet"
        elif parsed_ua.is_pc:
            device_type = "PC"
        else:
            device_type = "other"

        browser_family = parsed_ua.browser.family
        browser_version = parsed_ua.browser.version_string
        os_family = parsed_ua.os.family
        os_version = parsed_ua.os.version_string

        if parsed_ua.device.brand is None:
            device_brand = "-"
        else:
            device_brand = parsed_ua.device.brand
        
        if parsed_ua.device.model is None:
            device_model = "-"
        else:
            device_model = parsed_ua.device.model

        user_info = (device_type, device_brand,
                     device_model, os_family, os_version,
                     browser_family, browser_version
                     )
        parsed_ua_list.append(user_info)

    return parsed_ua_list


if __name__ == "__main__":
    raw = open_logfile("logs/logfile1.log")
    logs = get_all_logs(raw)
    print(logs[0])
    print(logs[1])
    print(logs[2])
    print(logs[3])
