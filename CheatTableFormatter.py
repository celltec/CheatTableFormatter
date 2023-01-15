import os
from argparse import ArgumentParser
from dataclasses import dataclass, field
import xml.etree.ElementTree as ET

@dataclass
class CheatEntry:
    description: str = 'N/A'
    children: list = field(default_factory=list)

def parse_cheat_entries(et_entries: ET.Element) -> list[CheatEntry]:
    entries = []
    for et_entry in et_entries:
        entry = CheatEntry()

        if (description := et_entry.find('Description')) is not None:
            entry.description = description.text.replace('"', '')

        if (children := et_entry.find('CheatEntries')) is not None:
            entry.children = parse_cheat_entries(children)

        entries.append(entry)
    return entries

def print_cheat_entry(entry: CheatEntry, depth: int = 0):
    print(entry.description)
    if entry.children:
        depth += 1
        space = '│  ' * (depth - 1)
        for child in entry.children[:-1]:
            print(f'{space}├─ ', end='')
            print_cheat_entry(child, depth)
        print(f'{space}└─ ', end='')
        print_cheat_entry(entry.children[-1], depth)

def main():
    parser = ArgumentParser(description='Print out an overview of a given cheat table')
    parser.add_argument('file', type=str, help='Path to cheat table')
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f'{args.file} is not a file')

    try:
        if entries := ET.parse(args.file).getroot().find('CheatEntries'):
            cheat_table = parse_cheat_entries(entries)
            for entry in cheat_table:
                print_cheat_entry(entry)
    except ET.ParseError:
        print(f'"{args.file}" is corrupted')

if __name__ == '__main__':
    main()
