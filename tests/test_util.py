# SPDX-FileCopyrightText: 2022 Magenta ApS
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import call
from unittest.mock import MagicMock

from konserver import util
from konserver.models import ObjectIdentifier
from konserver.models import Resource


def test_parse_conserves() -> None:
    namespace = "default"
    conserves = "configmaps.v1/foo,storage.k8s.io/v1/csidrivers/bar"
    actual = util.parse_conserves(namespace, conserves)
    expected = [
        ObjectIdentifier(namespace=namespace, resource="configmaps.v1", name="foo"),
        ObjectIdentifier(
            namespace=namespace, resource="storage.k8s.io/v1/csidrivers", name="bar"
        ),
    ]
    assert actual == expected


def test_parse_empty_conserves() -> None:
    assert util.parse_conserves(namespace="default", conserves=None) == []


def test_multi_handler() -> None:
    kopf_decorator = MagicMock()
    resources = [
        Resource(group="", version="v1", name="configmaps"),
        Resource(group="storage.k8s.io", version="v1", name="csidrivers"),
    ]
    func = MagicMock()

    util.multi_handler(kopf_decorator, resources, x=1, y=2)(func)

    assert kopf_decorator.call_args_list == [
        call("", "v1", "configmaps", x=1, y=2),
        call("storage.k8s.io", "v1", "csidrivers", x=1, y=2),
    ]
    func.assert_not_called()
