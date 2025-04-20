class UserAgents:

    def __init__(self, *args):
        """"
                0 — device type\n
                1 — device brand\n
                2 — device model\n
                3 — operating system\n
                4 — OS version\n
                5 — browser type\n
                6 — browser version\n
        """
        self.device_type = args[0]
        self.device_brand = args[1]
        self.device_model = args[2]
        self.os = args[3]
        self.os_version = args[4]
        self.browser_type = args[5]
        self.browser_version = args[6]
        self.all = args

    def __repr__(self):
        return str(self.all)

    def to_dict(self):
        return {
            "device_type"       : self.device_type,
            "device_brand"      : self.device_brand,
            "device_model"      : self.device_model,
            "os"                : self.os,
            "os_version"        : self.os_version,
            "browser_type"      : self.browser_type,
            "browser_version"   : self.browser_version,
        }