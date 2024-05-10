import argparse
import json

import inquirer
from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor

from tools import util
from tools.action import Action


class ExportSettings(Action):
    name = 'export-settings'
    prompt = 'Export Settings'

    def setup(self, parser: argparse.ArgumentParser):
        parser.add_argument('-o', '--output')

    def run(self, args: argparse.Namespace):
        if not args.output:
            if inquirer.confirm('Do you want to export the settings to a file?'):
                answer = inquirer.shortcuts.path('Enter the file path to export the settings to', 'output.json')
                setattr(args, 'output', answer)

        settings = util.get_settings()
        exported = {'tab_index': settings.value('tab_index')}
        for group in ['gen3', 'gen4', 'gen5', 'custom', 'action', 'updates', 'theme', 'timer']:
            self.__export_group(settings, group, exported)

        output = json.dumps(exported, indent=2)
        if args.output:
            with open(args.output, 'w') as file:
                file.write(output)
            return
        print(output)

    @classmethod
    def __export_group(cls, settings: QSettings, name: str, parent: any):
        m_group = {}
        parent[name] = m_group
        settings.beginGroup(name)
        for child_key in settings.childKeys():
            if name == 'action' and child_key == 'color':
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
            cls.__export_group(settings, child_group, m_group)
        settings.endGroup()
