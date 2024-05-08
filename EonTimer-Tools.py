#!/usr/bin/env python3

from enum import StrEnum

import inquirer
from PySide6.QtCore import QSettings


def main():
    # define actions
    class Action(StrEnum):
        RESET_SETTINGS = 'Reset settings'

    # prompt user for action
    answers = inquirer.prompt([
        inquirer.List(Action.__name__, 'Select an action', list(Action))
    ])
    action = answers[Action.__name__]

    # perform action
    actions = {
        Action.RESET_SETTINGS: do_reset_settings
    }
    actions[action]()


def do_reset_settings():
    if inquirer.confirm('Are you sure you want to reset the settings? This action cannot be undone.'):
        settings = QSettings(
            QSettings.defaultFormat(),
            QSettings.Scope.UserScope,
            'io.github.dasampharos',
            'EonTimer'
        )
        settings.clear()
        settings.sync()


if __name__ == '__main__':
    main()
