import json
from pikepdf import OutlineItem
from pathlib import Path
from pdf_add_outline.main import (
    json_to_outline,
    serialise_nested_tree,
    plaintext_to_outline,
)

SERIALISED_OUTPUT = [
    "Series Foreword, 11",
    "Foreword by William F. Hanks, 13",
    "Acknowledgments, 25",
    "1. Legitimate Peripheral Participation, 27",
    "    From apprenticeship to situated learning, 32",
    "    From situated learning to legitimate peripheral participation, 34",
    "    An analytic perspective on learning, 37",
    "    With legitimate peripheral participation, 39",
    "    The organization of this monograph, 42",
    "2. Practice, Person, Social World, 45",
    "    Internalization of the cultural given, 47",
    "    Participation in social practice, 49",
    "    The person and identity in learning, 52",
    "    The social world, 54",
    "3. Midwives, Tailors, Quartermasters, Butchers, Nondrinking Alcoholics, 59",
    "    The case of apprenticeship, 62",
    "    Five studies of apprenticeship, 65",
    "    The apprenticeship of Yucatec midwives, 67",
    "    The apprenticeship of Vai and Gola tailors, 69",
    "    The apprenticeship of naval quartermasters, 73",
    "    The apprenticeship of meat cutters, 76",
    "    The apprenticeship of nondrinking alcoholics, 79",
    "    Apprenticeship and situated learning: A new agenda, 84",
    "4. Legitimate Peripheral Participation in Communities of Practice, 89",
    "    Structuring resources for learning in practice, 91",
    "    The place of knowledge: Participation, learning curricula, communities of practice, 94",
    "    The problem of access: Transparency and sequestration, 100",
    "    Discourse and practice, 105",
    "    Motivation and identity: Effects of participation, 110",
    "    Contradictions and change: Continuity and displacement, 113",
    "5. Conclusion, 119",
    "References, 125",
    "Index, 131",
]


def test_serialised_nested_tree_basic():
    outline_items = [
        OutlineItem("Chapter 1", 1),
        OutlineItem("Chapter 2", 2),
        OutlineItem("Chapter 3", 3),
        OutlineItem("Chapter 4", 4),
    ]

    assert serialise_nested_tree(outline_items) == [
        "Chapter 1, 1",
        "Chapter 2, 2",
        "Chapter 3, 3",
        "Chapter 4, 4",
    ]


def test_serialised_nested_tree_nested():
    outline_children_children = [
        OutlineItem("1.1.1", 1),
        OutlineItem("1.1.2", 1),
        OutlineItem("1.1.3", 1),
        OutlineItem("1.1.4", 1),
    ]
    outline_children = [
        OutlineItem("1.1", 1),
        OutlineItem("1.2", 2),
        OutlineItem("1.3", 3),
        OutlineItem("1.4", 4),
    ]
    outline_items = [
        OutlineItem("Chapter 1", 1),
        OutlineItem("Chapter 2", 5),
        OutlineItem("Chapter 3", 6),
        OutlineItem("Chapter 4", 7),
    ]
    outline_children[0].children = outline_children_children
    outline_items[0].children = outline_children

    assert serialise_nested_tree(outline_items) == [
        "Chapter 1, 1",
        "    1.1, 1",
        "        1.1.1, 1",
        "        1.1.2, 1",
        "        1.1.3, 1",
        "        1.1.4, 1",
        "    1.2, 2",
        "    1.3, 3",
        "    1.4, 4",
        "Chapter 2, 5",
        "Chapter 3, 6",
        "Chapter 4, 7",
    ]


def test_json_to_outline():
    parent = Path(__file__).parent
    toc_source = parent / "fixtures" / "situated_learning.json"
    toc_source_json = json.loads(toc_source.read_text())

    assert (
        serialise_nested_tree(json_to_outline(toc_source_json, 0)) == SERIALISED_OUTPUT
    )


def test_plaintext_to_outline():
    parent = Path(__file__).parent
    toc_source = parent / "fixtures" / "situated_learning.txt"

    assert (
        serialise_nested_tree(
            plaintext_to_outline(toc_source.read_text().splitlines(), 0)
        )
        == SERIALISED_OUTPUT
    )
