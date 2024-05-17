class SizeError(Exception):
    def __init__(self):
        message = 'Data size out of range!!!'
        super().__init__(message)
