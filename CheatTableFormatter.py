import os
import treelib
from typing import Optional
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

def add_entry_to_tree(tree: treelib.Tree, entry: CheatEntry, parent: Optional[str] = None):
    node = treelib.Node(entry.description)
    tree.add_node(node, parent)
    for child in entry.children:
        add_entry_to_tree(tree, child, node.identifier)

def main():
    parser = ArgumentParser(description='Print out an overview of a given cheat table')
    parser.add_argument('file', type=str, help='Path to cheat table')
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f'{args.file} is not a file')

    if entries := ET.parse(args.file).getroot().find('CheatEntries'):
        cheat_table = parse_cheat_entries(entries)
        tree = treelib.Tree()
        add_entry_to_tree(tree, CheatEntry('CheatTable', cheat_table))  # Need a root node containing all entries
        tree.show()

if __name__ == '__main__':
    main()
