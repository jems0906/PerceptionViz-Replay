from __future__ import annotations

import json
from pathlib import Path

from mcap.reader import make_reader


def import_messages(path: Path) -> list[dict]:
    with path.open("rb") as stream:
        reader = make_reader(stream)
        return [json.loads(message.data.decode()) for _, _, message in reader.iter_messages()]
