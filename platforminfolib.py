def subprocess_postproc(x):
    return x.stdout.read().strip().decode("utf-8")


class PlatformError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def Parser(filename, to_be_cut, basestr):
    with open(filename) as file:
        x = dict()
        for line in file:
            x[line.split("=")[0]] = line.split(to_be_cut)[1]

        version = x[basestr].strip()
    return version
