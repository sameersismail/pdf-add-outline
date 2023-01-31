# `pdf-add-outline`

Add an outline to a PDF file. What it says on the tin.

# Installation

Install through `pip`:

```
pip install pdf-add-outline
```

# Usage

```
$ pdf-add-outline --help
usage: pdf-add-outline [-h] -o OUTPUT [-d] [--increment INCREMENT] <pdf_file> <toc_file>

Add an outline to a PDF.

positional arguments:
  <pdf_file>            Input PDF
  <toc_file>            JSON- or TXT-encoded ToC file (file type suffix required)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Resultant filename (required)
  -d, --dry             Output the parsed OutlineItem structure; don't touch the PDF
  --increment INCREMENT
                        Increase all entries by <increment> amount
```

## Example

```
$ pdf-add-outline tests/fixtures/Situated_Learning.pdf tests/fixtures/situated_learning.txt -o situated_with_outline.pdf
```

## ToC File Formats

```
$ head tests/fixtures/situated_learning.json
[
    ["Series Foreword", 11, []],
    ["Foreword by William F. Hanks", 13, []],
    ["Acknowledgments", 25, []],
    ["1. Legitimate Peripheral Participation", 27, [
        ["From apprenticeship to situated learning", 32, []],
        ["From situated learning to legitimate peripheral participation", 34, []],
        ["An analytic perspective on learning", 37, []],
        ["With legitimate peripheral participation", 39, []],
        ["The organization of this monograph", 42, []]
```

```
$ head tests/fixtures/situated_learning.txt
Series Foreword, 11
Foreword by William F. Hanks, 13
Acknowledgments, 25
1. Legitimate Peripheral Participation, 27
    From apprenticeship to situated learning, 32
    From situated learning to legitimate peripheral participation, 34
    An analytic perspective on learning, 37
    With legitimate peripheral participation, 39
    The organization of this monograph, 42
2. Practice, Person, Social World, 45
```

# Development

1. Prerequisites: Clone the repository. Install [Poetry](https://python-poetry.org/).
2. Run `poetry install` in the root of the directory.
3. Run the tests.

   ```
   $ poetry run pytest tests
   collected 4 items

   tests/test_parsing.py ....        [100%]

   ========== 4 passed in 0.03s ===========
   ```

4. Run `mypy`.

   ```
   $ poetry run mypy pdf_add_outline tests
   Success: no issues found in 4 source files
   ```

5. Run `black`.

   ```
   $ poetry run black pdf_add_outline tests
   All done! ✨ 🍰 ✨
   4 files left unchanged.
   ```

# Acknowledgements

The excellent [PikePDF](https://github.com/pikepdf/pikepdf) package, which wraps the [QPDF](https://github.com/qpdf/qpdf) library. Jean Lave and Etienne Wenger's _Situated Learning_ for the example (and test) table of contents.
