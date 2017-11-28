class Status:
    def __init__(self):
        self.name = None
        self.hostname = None
        self.port = None

    def __str__(self):
        return "{} is running on {}:{}".format(
            self.name, self.hostname, self.port
        )
