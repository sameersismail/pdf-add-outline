from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass
from pikepdf import Pdf, OutlineItem


class IndentationError(Exception):
    ...


@dataclass
class TOCItem:
    toc_item: str
    page_num: int
    num_indents: int


FileItem = Tuple[str, int, List["FileItem"]]


def replace_outline(
    input_pdf_filename: Path, new_outline: List[OutlineItem], output_file: Path
):
    pdf = Pdf.open(input_pdf_filename)
    with pdf.open_outline() as outline:
        outline.root.clear()
        outline.root.extend(new_outline)
    pdf.save(output_file)


def json_to_outline(file_items: List[FileItem], increment: int) -> List[OutlineItem]:
    def recurse(file_item: FileItem) -> OutlineItem:
        if len(file_item[2]) == 0:
            return OutlineItem(file_item[0], file_item[1])
        else:
            children = []
            for child in file_item[2]:
                children.append(recurse(child))
            outline_item = OutlineItem(file_item[0], file_item[1] + increment)
            outline_item.children = children
            return outline_item

    outline_items: List[OutlineItem] = []
    for file_item in file_items:
        outline_items.append(recurse(file_item))
    return outline_items


def plaintext_to_outline(lines: List[str], increment: int) -> List[OutlineItem]:
    lines = [line for line in lines if line != "" and "," in line]
    toc_items = construct_toc_items(lines)
    validate_indentation(toc_items)
    return toc_items_to_outline(toc_items, increment)


def construct_toc_items(toc_lines: List[str]) -> List[TOCItem]:
    toc_items: List[TOCItem] = []
    for line in toc_lines:
        *toc_line_items, page_num = line.rsplit(",", maxsplit=1)
        toc_item = " ".join(toc_line_items)
        indents = toc_item.split("    ")
        toc_items.append(
            TOCItem(
                toc_item=indents[-1],
                page_num=int(page_num),
                num_indents=len(indents),
            )
        )
    return toc_items


def validate_indentation(toc_lines: List[TOCItem]) -> None:
    for i in range(1, len(toc_lines)):
        if (toc_lines[i].num_indents - toc_lines[i - 1].num_indents) > 1:
            raise IndentationError(
                f"Syntactic structure flouted; offending items: "
                f"'{toc_lines[i - 1].toc_item}' & '{toc_lines[i].toc_item}'"
            )


def toc_items_to_outline(toc_items: List[TOCItem], increment: int) -> List[OutlineItem]:
    def recurse() -> OutlineItem:
        nonlocal index  # type: ignore
        toc_item = toc_items[index]
        outline_item = OutlineItem(toc_item.toc_item, toc_item.page_num + increment)
        children = []

        while (index + 1) < len(toc_items):
            if toc_items[index + 1].num_indents == (toc_item.num_indents + 1):
                index += 1
                if index < len(toc_items):
                    children.append(recurse())
            else:
                break
        outline_item.children = children

        return outline_item

    outline_items, index = [], 0
    while index < len(toc_items):
        outline_items.append(recurse())
        index += 1
    return outline_items


def serialise_nested_tree(outline_items: List[OutlineItem]) -> List[str]:
    def preorder(outline_item: OutlineItem):
        nonlocal indent  # type: ignore
        buffer.append(f"{' ' * indent}{outline_item.title}, {outline_item.destination}")
        indent += 4
        for child in outline_item.children:
            preorder(child)
        indent -= 4

    buffer: List[str]
    buffer, indent = [], 0
    for outline_item in outline_items:
        preorder(outline_item)

    return buffer
