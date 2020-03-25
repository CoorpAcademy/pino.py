#!/usr/bin/env python
import json
import fileinput
from datetime import datetime
import style

def main():
    # note: this is a proto for now. Configurability yo be set up!
    for line in fileinput.input():
        try:
            log = json.loads(line)
            level = log.get("level", "info")
            time = log["time"]
            message = log["message"]
            millidiff = log["millidiff"]
            when = datetime.fromtimestamp(time/1000)
            # TODO: add list of meta to (conditionnaly extract)

            print(
                style.magenta(when),
                style.blue.bold(level).rjust(8),
                message.ljust(80), # TODO: make it based on TTY width
                style.red.bold(f"+{millidiff}ms")
            )
        except json.decoder.JSONDecodeError:
            print(line.rstrip())
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
