# 공개 README 6개 언어와 NOTICE (PRD §2.6·§5, D019, D031). 형식은 metarche readme 표준을 따른다.
import re

import pytest
from test_generate import _REPO

_READMES = ["README.md", "README.ko.md", "README.zh-CN.md", "README.ja.md", "README.es.md", "README.ru.md"]
_NOTICE_LINE = {
    "README.ko.md": "이 문서는 영어판을 AI로 번역한 것입니다. 내용이 다르면 영어판을 따릅니다.",
    "README.zh-CN.md": "本文档由 AI 从英文版翻译而来。如有出入，以英文版为准。",
    "README.ja.md": "この文書は英語版を AI で翻訳したものです。内容が異なる場合は英語版に従ってください。",
    "README.es.md": "Este documento es una traducción automática con IA de la versión en inglés. Si hay diferencias, prevalece la versión en inglés.",
    "README.ru.md": "Этот документ переведён с английской версии с помощью ИИ. При расхождениях ориентируйтесь на английскую версию.",
}
_SOURCES = ["unslop", "CC BY 4.0", "Hallmark", "Impeccable", "Taste Skill", "qt-ui-design", "winui-design",
            "native-feel", "platform-design-skills", "clig.dev"]
_FORBIDDEN = [r"[A-Za-z]:\\Users\\", r"/Users/\w", r"[\w.+-]+@[\w-]+\.[\w.]+", r"\b\d{1,3}(\.\d{1,3}){3}\b"]
def _read(name: str) -> str:
    return (_REPO / name).read_text(encoding="utf-8")


def _shape(text: str) -> tuple[int, int]:
    return sum(line.startswith("## ") for line in text.splitlines()), text.count("img.shields.io/")


@pytest.mark.parametrize("name", _READMES)
def test_language_line_links_every_readme(name):
    head = "\n".join(_read(name).splitlines()[:12])
    assert all(f'href="{other}"' in head for other in _READMES)


@pytest.mark.parametrize("name", _READMES[1:])
def test_translation_has_notice_and_same_shape(name):
    text = _read(name)
    assert _NOTICE_LINE[name] in text
    assert _shape(text) == _shape(_read("README.md"))


@pytest.mark.parametrize("name", _READMES)
def test_relative_links_point_to_files(name):
    text = _read(name)
    targets = re.findall(r'\]\(([^)\s#]+)', text) + re.findall(r'(?:href|src)="([^"#]+)"', text)
    missing = [t for t in targets if "://" not in t and not (_REPO / t).exists()]
    assert missing == []


@pytest.mark.parametrize("name", [*_READMES, "NOTICE"])
def test_no_private_information(name):
    text = _read(name)
    assert [p for p in _FORBIDDEN if re.search(p, text)] == []


@pytest.mark.parametrize("name", ["NOTICE"])
def test_notice_names_every_source(name):
    text = _read(name)
    assert [s for s in _SOURCES if s not in text] == []
