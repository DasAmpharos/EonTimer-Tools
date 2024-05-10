#!/usr/bin/env python3
import json
from enum import StrEnum

import inquirer
from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor


def main():
    # define actions
    class Action(StrEnum):
        EXPORT_SETTINGS = 'Export Settings'
        RESET_SETTINGS = 'Reset settings'

    # prompt user for action
    answers = inquirer.prompt([
        inquirer.List(Action.__name__, 'Select an action', list(Action))
    ])
    action = answers[Action.__name__]

    # perform action
    actions = {
        Action.EXPORT_SETTINGS: export_settings,
        Action.RESET_SETTINGS: reset_settings
    }
    actions[action]()


def export_settings():
    answers = inquirer.prompt([
        inquirer.Path('file', 'output.json',
                      path_type=inquirer.Path.FILE,
                      message='Enter the file path to export the settings to')
    ])

    settings = QSettings(
        QSettings.defaultFormat(),
        QSettings.Scope.UserScope,
        'io.github.dasampharos',
        'EonTimer'
    )

    def export_group(name: str, parent: any):
        m_group = {}
        parent[name] = m_group
        settings.beginGroup(name)
        for child_key in settings.childKeys():
            if group == 'action' and child_key == 'color':
                value: QColor = settings.value(child_key, type=QColor)
                m_group[child_key] = {
                    'r': value.red(),
                    'g': value.green(),
                    'b': value.blue(),
                    'a': value.alpha()
                }
            else:
                m_group[child_key] = settings.value(child_key)
        for child_group in settings.childGroups():
            export_group(child_group, m_group)
        settings.endGroup()

    exported = {'tab_index': settings.value('tab_index')}
    settings_groups = {
        'timers': [
            'gen3',
            'gen4',
            'gen5',
            'custom'
        ],
        'settings': [
            'action',
            'updates',
            'theme',
            'timer'
        ]
    }
    for group_type, groups in settings_groups.items():
        m_exported = {}
        for group in groups:
            export_group(group, m_exported)
        exported[group_type] = m_exported

    with open(answers['file'], 'w') as file:
        json.dump(exported, file, indent=2)


def reset_settings():
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
