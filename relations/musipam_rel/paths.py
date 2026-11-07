"""Where things live. Generated data and trained weights stay outside Google Drive and git."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # v2/relations
STIMULI = ROOT.parent / "stimuli"                    # the musiPAM stimulus set
STIMGEN = ROOT.parent / "stimgen"                    # the stimulus generator (for its design check)
DATA = Path(os.environ.get("MUSIPAM_REL_DATA", Path.home() / "musipam-data" / "relations"))
MODELS = DATA / "models"
REPORTS = ROOT / "reports"
EXAMPLES = ROOT / "examples"
