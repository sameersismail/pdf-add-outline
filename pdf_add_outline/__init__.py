import json
import argparse
from typing import List
from pathlib import Path
from dataclasses import dataclass

from pdf_add_outline.main import (
    FileItem,
    json_to_outline,
    plaintext_to_outline,
    serialise_nested_tree,
    replace_outline,
)


@dataclass
class ProgramArguments:
    pdf_file: str
    toc_file: str
    output_file: str
    dry_run: bool = False
    increment: int = 0


def main() -> int:
    arguments = get_arguments()
    pdf_file, toc_file, output_file, dry_run = (
        Path(arguments.pdf_file),
        Path(arguments.toc_file),
        Path(arguments.output_file),
        arguments.dry_run,
    )
    toc_extension = toc_file.suffix

    with open(toc_file) as fd:
        outline_file = fd.read()

    if toc_extension == ".json":
        outline_json: List[FileItem] = json.loads(outline_file)
        outline = json_to_outline(outline_json, arguments.increment)
    elif toc_extension == ".txt" or toc_extension == "":
        outline = plaintext_to_outline(outline_file.splitlines(), arguments.increment)
    else:
        raise ValueError(f"Invalid filetype '{toc_extension}' for file '{toc_file}'.")

    if dry_run:
        for line in serialise_nested_tree(outline):
            print(line)
    else:
        replace_outline(pdf_file, outline, output_file)

    return 0


def get_arguments() -> ProgramArguments:
    parser = argparse.ArgumentParser(description="Add an outline to a PDF.")
    parser.add_argument("pdf_file", metavar="<pdf_file>", type=str, help="Input PDF")
    parser.add_argument(
        "toc_file",
        metavar="<toc_file>",
        type=str,
        help="JSON- or TXT-encoded ToC file (file type suffix required)",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=str,
        help="Resultant filename (required)",
    )
    parser.add_argument(
        "-d",
        "--dry",
        action="store_true",
        help="Output the parsed OutlineItem structure; don't touch the PDF",
    )
    parser.add_argument(
        "--increment",
        type=int,
        help="Increase all entries by <increment> amount",
    )
    args = parser.parse_args()

    return ProgramArguments(
        pdf_file=args.pdf_file,
        toc_file=args.toc_file,
        output_file=args.output,
        dry_run=args.dry,
        increment=args.increment or 0,
    )


if __name__ == "__main__":
    main()
