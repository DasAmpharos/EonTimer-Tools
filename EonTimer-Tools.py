#!/usr/bin/env python3

import argparse
import functools
import importlib
import pkgutil
from typing import Type, TypeVar

import inquirer

from tools.action import Action


def main():
    subclasses = find_subclasses('tools', Action)
    actions = {subclass.prompt: subclass() for subclass in subclasses}

    parser = argparse.ArgumentParser()
    default_action = functools.partial(interactive, actions)
    parser.set_defaults(func=default_action)
    subparsers = parser.add_subparsers()
    for action in actions.values():
        subparser = subparsers.add_parser(action.name, help=action.prompt)
        subparser.set_defaults(func=action.run)
        action.setup(subparser)
    args = parser.parse_args()
    args.func(args)


def interactive(actions: dict[str, Action],
                args: argparse.Namespace):
    answer = inquirer.list_input('Select an action', actions.keys())
    action = actions[answer]
    action.run(args)


T = TypeVar('T')


def find_subclasses(package: str, base_class: Type[T]) -> set[Type[T]]:
    subclasses: set[Type[T]] = set()
    for _, module_name, _ in pkgutil.iter_modules([package]):
        module = importlib.import_module(f'{package}.{module_name}')
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type) and issubclass(attribute, base_class) and attribute != base_class:
                subclasses.add(attribute)
    return subclasses


if __name__ == '__main__':
    main()
