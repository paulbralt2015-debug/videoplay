import re
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "twinsplayer"


def test_version_definie():
    import twinsplayer
    from twinsplayer._version import __version__
    assert re.fullmatch(r"\d+\.\d+\.\d+", __version__)
    assert twinsplayer.__version__ == __version__


def test_imports_du_paquet_existent():
    """Chaque « from . import X » / « from .X import ... » de app.py doit exister dans le paquet."""
    src = (SRC / "app.py").read_text(encoding="utf-8")
    for m in re.finditer(r"^from \. import ([^\n(]+)$", src, re.M):
        for name in [n.strip() for n in m.group(1).split(",")]:
            assert (SRC / f"{name}.py").exists(), name
    for m in re.finditer(r"^from \.(\w+) import", src, re.M):
        assert (SRC / f"{m.group(1)}.py").exists(), m.group(1)


def test_app_n_importe_pas_version_depuis_init():
    src = (SRC / "app.py").read_text(encoding="utf-8")
    assert not re.search(r"^from \. import .*__version__", src, re.M)
