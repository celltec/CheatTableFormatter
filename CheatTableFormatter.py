import os
from argparse import ArgumentParser
from dataclasses import dataclass, field
import xml.etree.ElementTree as ET

@dataclass
class CheatEntry:
    description: str = 'N/A'
    childreen: list = field(default_factory=list)

def parse_cheat_entries(et_entries: ET.Element) -> list[CheatEntry]:
    entries = []
    for et_entry in et_entries:
        entry = CheatEntry()
        for et_element in et_entry:
            match et_element.tag:
                case 'Description':
                    entry.description = et_element.text.replace('"', '')
                case 'CheatEntries':
                    entry.childreen = parse_cheat_entries(et_element)
        entries.append(entry)
    return entries

def print_cheat_table(table: list[CheatEntry]):
    # TODO

    test = [CheatEntry(description='DEBUG', childreen=[]),
            CheatEntry(description='SCRIPTS ▼',
                       childreen=[CheatEntry(description='INTERFACE', childreen=[]),
                                  CheatEntry(description='MATCH ▼',
                                             childreen=[CheatEntry(description='target',
                                                                   childreen=[])])])]
    assert table == test

def main():
    parser = ArgumentParser(description='Print out an overview of a given cheat table')
    parser.add_argument('file', type=str, help='Path to cheat table')
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f'{args.file} is not a file')

    try:
        if entries := ET.parse(args.file).getroot().find('CheatEntries'):
            print_cheat_table(parse_cheat_entries(entries))
    except ET.ParseError:
        print(f'"{args.file}" is corrupted')

if __name__ == '__main__':
    main()
