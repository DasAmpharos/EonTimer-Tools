import argparse
from abc import abstractmethod


class Action:
    name: str
    prompt: str

    @abstractmethod
    def setup(self, parser: argparse.ArgumentParser):
        ...

    @abstractmethod
    def run(self, args: argparse.Namespace):
        ...
