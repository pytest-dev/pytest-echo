from __future__ import annotations

import pytest_echo


def test_version() -> None:
    assert pytest_echo.__version__ is not None
