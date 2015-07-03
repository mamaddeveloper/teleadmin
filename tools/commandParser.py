

class CommandParser:
    def __init__(self, listValid):
        self.listValid = listValid

    def parse(self, text):
        text =str(text)
        if not text.startswith("/"):
            return self.invalid()
        parts = text.split(" ")
        args = ""
        if (len(parts) > 1):
            args = " ".join(parts[1:])
        cmd = parts[0][1:].lower()
        if "@" in cmd:
            cmd = cmd.split("@")[0]

        if len(cmd) <= 1:
            return self.invalid()

        if cmd not in self.listValid:
            return self.invalid()

        return CommandResult(True, cmd, args)

    @staticmethod
    def invalid():
        return CommandResult(False)

class CommandResult:
    def __init__(self, isValid, command="", args=""):
        self.isValid = isValid
        self.command = command
        self.args = args
