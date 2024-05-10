import argparse

import inquirer

from tools import util
from tools.action import Action


class ResetSettings(Action):
    name = 'reset-settings'
    prompt = 'Reset Settings'

    def setup(self, parser: argparse.ArgumentParser):
        parser.add_argument('-y', '-Y',
                            dest='confirmed',
                            action='store_true',
                            help='Skip confirmation')

    def run(self, args: argparse.Namespace):
        if not args.confirmed:
            answer = inquirer.confirm('Are you sure you want to reset the settings? This action cannot be undone.')
            setattr(args, 'confirmed', answer)
        if args.confirmed:
            settings = util.get_settings()
            settings.clear()
            settings.sync()
