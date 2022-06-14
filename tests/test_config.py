# SPDX-FileCopyrightText: 2022 Magenta ApS
# SPDX-License-Identifier: MPL-2.0
import json

from _pytest.monkeypatch import MonkeyPatch

from konserver.config import Config
from konserver.models import Resource


def test_nested_delimiter(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("ANNOTATION__PREFIX", "foo")
    assert Config().annotation.prefix == "foo"


def test_watched_resources(monkeypatch: MonkeyPatch) -> None:
    watched_resources = [
        {"group": "", "name": "configmaps", "version": "v1"},
        {"group": "storage.k8s.io", "name": "csidrivers", "version": "v1"},
    ]
    monkeypatch.setenv("WATCHED_RESOURCES", json.dumps(watched_resources))
    assert Config().watched_resources == [
        Resource(group="", version="v1", name="configmaps"),
        Resource(group="storage.k8s.io", version="v1", name="csidrivers"),
    ]
