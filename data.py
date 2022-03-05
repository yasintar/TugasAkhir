class Data:
    def __init__(self, sender, receiver, dfile, filename=None, filesize=65536):
        self.sender = sender
        self.receiver = receiver
        self.filename = filename
        self.file = dfile
        self.filesize = filesize