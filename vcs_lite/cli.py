from tabulate import tabulate
from __version__ import __version__

from abc import ABC, abstractmethod
from argparse import ArgumentParser
from settings import Settings
from updater import Updater

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

        self.parser.add_argument('--version', action='version', version='%(prog)s {version}\n'.format(version=__version__))
        sub_parsers = self.parser.add_subparsers(dest="subcmd", help="commands")

        UpdateCmd(sub_parsers)
        ListRepositories(sub_parsers)
    # end


    def execute(self):
        try:
            args = self.parser.parse_args()

            args.func(args)

        except Exception as e:
            self.parser.print_help()
            raise e
        # end
    # end
# end

class ListRepositories(Subcommand):
    def __init__(self, subparser):
        super().__init__(name="list", aliases=['u'],
                         help='prints a list of all configured repositories', subparser=subparser)
        self.settings = Settings()
    # end

    def setup(self, subparser):
        super().setup(subparser)
    # end

    def execute(self, args):
        loaded_settings = self.settings.load_settings()

        if (not loaded_settings):
            print("couldn't load settings")
            return
        # end

        repos = [[item['label'], item['vcs']['program'], item['enabled']] for item in loaded_settings['toUpdate']]
        headers = ['Repo', 'VCS', 'enabled']

        print(tabulate(repos, headers=headers))


class UpdateCmd(Subcommand):

    def __init__(self, subparser):
        super().__init__(name="update", aliases=["u"],
                         help="bulk update all configured repos", subparser=subparser)
    # end


    def setup(self, subparser):
        super().setup(subparser)

        self.cmd_parser.add_argument('-v', '--verbose', action='store_true', help='print more infos')
        self.cmd_parser.add_argument('-r', '--repo', dest="repos", type=str, nargs='+',
                                     help="list of repos to update")

    # end

    def execute(self, args):
        print("updating now...")

        if args.repos:
            for repo in args.repos:
                print("*", repo)
            # end
        else:
            updater = Updater()
            updater.update_all()
        # end
    # end
# end
