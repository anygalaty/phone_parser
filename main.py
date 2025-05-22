import re
from typing import Iterator
import click


class PhoneExtractor:
    PHONE_PATTERN = re.compile(r"(?:(?:\+7|8)[\s\-\.]*)\(?(\d{3})\)?[\s\-\.]*(\d{3})[\s\-\.]*(\d{2})[\s\-\.]*(\d{2})")

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.text = self._read_file()

    def _read_file(self) -> str:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read()

    def extract(self) -> Iterator[str]:
        seen = set()
        for match in self.PHONE_PATTERN.finditer(self.text):
            phone = f"+7({match.group(1)}){match.group(2)}-{match.group(3)}-{match.group(4)}"
            if phone not in seen:
                seen.add(phone)
                yield phone

    def run(self) -> None:
        for phone in self.extract():
            print(phone)


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
def main(filepath: str) -> None:
    extractor = PhoneExtractor(filepath)
    extractor.run()


if __name__ == "__main__":
    main()
