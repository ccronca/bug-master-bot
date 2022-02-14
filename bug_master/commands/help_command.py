from typing import Dict

from loguru import logger
from starlette.responses import Response

from .. import consts
from .command import Command


class HelpCommand(Command):
    @classmethod
    def get_arguments_info(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def get_description(cls) -> str:
        return "More information about how to use Bot Master"

    @classmethod
    def get_commands_info(cls) -> str:
        from .command_handler import SupportedCommands

        commands_map = SupportedCommands.get_commands_map()
        commands = list(commands_map.keys())
        commands_cls = list(commands_map.values())
        commands_info = []

        for i in range(len(commands)):
            command_str = [f"{i + 1}. {commands[i]} - {commands_cls[i].get_description()}"]

            for argument, arg_info in commands_cls[i].get_arguments_info().items():
                command_str += [f"\t{u'•'} {argument}: {arg_info}"]

            commands_info.append("\n".join(command_str))

        return "\n".join(commands_info)

    async def handle(self) -> Response:
        logger.info(f"Handling {self._command}")

        return self.get_response(
            f"*============== Help ==============*\n"
            f"*Available commands:*\n"
            f"```{self.get_commands_info()}```\n\n"
            f"*Configuration file:*\n"
            f"Bot configuration file, defines each job action on failure. The configuration file name must be named"
            f" `{consts.CONFIGURATION_FILE_NAME}`.\n"
            f"For each action (job failure) this are the following arguments:\n"
            f"``` 1. description  - Description of the failure.\n"
            f" 2. emoji - Reaction to add to the thread on case of match (If empty or missing no reaction "
            f"is posted).\n"
            f" 3. text -  Comment to add to thread on case of match (If empty or missing, no comment is posted)\n"
            f" 4. contains - String that indicates the failure, checks if any files content that listed on "
            f"`file_path` contains that given string.\n"
            f" 6. file_path  - File or directory to search for match in it. The path is relative to PROW job"
            f" (starting with artifacts). To specify a directory just set file name to be *.```\n"
        )
