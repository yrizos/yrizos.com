from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path


class FakePixmap:
    def __init__(self, colorspace_name: str = "RGB") -> None:
        self.colorspace = SimpleNamespace(name=colorspace_name)

    def save(self, output_path, output=None):
        output_path.write_bytes(b"png-bytes")


class FakePage:
    def __init__(self) -> None:
        self.rect = SimpleNamespace(width=200)

    def get_pixmap(self, matrix, alpha=False):
        return FakePixmap()


class FakeDocument:
    def __init__(self) -> None:
        self.pages = [FakePage()]

    def __len__(self):
        return len(self.pages)

    def __getitem__(self, index):
        return self.pages[index]

    def close(self):
        return None


class SimpleNamespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_pdf_to_images_creates_pngs(monkeypatch, tmp_path: Path) -> None:
    fake_fitz = types.SimpleNamespace(
        csRGB=SimpleNamespace(name="RGB"),
        Matrix=lambda x, y: (x, y),
        Pixmap=lambda colorspace, pix: pix,
        open=lambda pdf_path: FakeDocument(),
    )
    monkeypatch.setitem(sys.modules, "fitz", fake_fitz)

    import scripts.pdf_to_images as pdf_mod
    importlib.reload(pdf_mod)

    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n")
    output_dir = tmp_path / "images"

    pdf_mod.pdf_to_images(pdf_path, output_dir, prefix="slide")

    assert (output_dir / "slide-01.png").exists()
    assert (output_dir / "slide-01.png").read_bytes() == b"png-bytes"


def test_pdf_to_images_main_uses_cli_args(monkeypatch, tmp_path: Path) -> None:
    import scripts.pdf_to_images as pdf_mod

    captured = {}

    def fake_pdf_to_images(pdf_path, output_dir, dpi=300, prefix=None):
        captured["path"] = pdf_path
        captured["output"] = output_dir
        captured["dpi"] = dpi
        captured["prefix"] = prefix

    monkeypatch.setattr(pdf_mod, "pdf_to_images", fake_pdf_to_images)
    monkeypatch.setattr(sys, "argv", ["pdf_to_images.py", str(tmp_path / "input.pdf"), "-o", str(tmp_path / "out"), "-d", "200", "-p", "custom"])

    pdf_mod.main()

    assert captured["path"] == (tmp_path / "input.pdf").resolve()
    assert captured["output"] == (tmp_path / "out").resolve()
    assert captured["dpi"] == 200
    assert captured["prefix"] == "custom"


def test_fetch_posts_script_wrapper(monkeypatch) -> None:
    import runpy
    import sys
    import types

    calls = []
    fake_posts = types.SimpleNamespace(main=lambda: calls.append("main"))
    monkeypatch.setitem(sys.modules, "posts", fake_posts)
    script_path = Path(__file__).parents[1] / "scripts" / "fetch_posts.py"
    runpy.run_path(script_path, run_name="__main__")
    assert calls == ["main"]
