from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def ensure_sample_catalog(
    csv_path: Path, generator_script: Path, count: int = 5000
) -> bool:
    if csv_path.is_file():
        return False
    if not generator_script.is_file():
        raise FileNotFoundError(f"Sample catalog generator not found: {generator_script}")
    subprocess.run(
        [
            sys.executable,
            str(generator_script),
            "--count",
            str(count),
            "--output",
            str(csv_path),
        ],
        check=True,
        cwd=generator_script.resolve().parents[1],
    )
    return True