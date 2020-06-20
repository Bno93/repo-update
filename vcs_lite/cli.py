

from argparse import ArgumentParser
from abc import ABC, abstractmethod


def make_command(setup):

    """
    decorator to setup basic subcommand infos

    will set the command, name, aliases and help text
    """
    def wrapper(self, subparser):
        self.cmd_parser = subparser.add_parser(self.cmd_name,
                                               aliases=self.cmd_aliases, help=self.cmd_help)
        setup(self, subparser)

    # end
    return wrapper


class Subcommand(ABC):
    """ Class with provide basic Features to build a Subcommands """

    @abstractmethod
    def __init__(self, **kwargs):
        self.cmd_name = kwargs["name"]
        self.cmd_aliases = kwargs["aliases"]
        self.cmd_help = kwargs["help"]
        self.cmd_parser = None
        self.setup(kwargs["subparser"])

    # @abstractmethod
    @make_command
    def setup(self, subparser):
        """
        setup the sub command parser

        sets the function with will exetuted by the argparse framework
        """
        self.cmd_parser.set_defaults(func=self.execute)

    @abstractmethod
    def execute(self, args):
        pass
    # end


    def get_aliases(self):
        """ generator for all names of the command eihter name or aliases """
        yield self.cmd_name
        yield from self.cmd_aliases
    # end
# end

class Cli():

    def __init__(self):

        self.parser = ArgumentParser("vcs-lite",
                                "vcs-lite [COMMAND] [OPTION]", "cli for bulk updating repositories")

        sub_parsers = self.parser.add_subparsers(dest="subcmd", help="commands")

        UpdateCmd(sub_parsers)
    # end


    def execute(self):
        try:
            args = self.parser.parse_args()

            args.func(args)

        except Exception as e:
            self.parser.print_help()
            raise e
# end



class UpdateCmd(Subcommand):

    def __init__(self, subparser):
        super().__init__(name="update", aliases=["u"],
                         help="bulk update all configured repos", subparser=subparser)
    # end


    def setup(self, subparser):
        super().setup(subparser)

        self.cmd_parser.add_argument('-r', '--repo', dest="repos", type=str, nargs='+',
                                     help="list of repos to update")

    # end

    def execute(self, args):
        print("updating now...")

        if args.repos:
            for repo in args.repos:
                print("*", repo)
            # end
        # end
    # end
# end
