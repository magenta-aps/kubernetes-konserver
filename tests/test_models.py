# SPDX-FileCopyrightText: 2022 Magenta ApS
# SPDX-License-Identifier: MPL-2.0
import kopf

from konserver.models import ObjectIdentifier


def test_object_identifier_equality() -> None:
    a = ObjectIdentifier(namespace="1", resource="2", name="3")
    b = ObjectIdentifier(namespace="1", resource="2", name="3")
    c = ObjectIdentifier(namespace="4", resource="5", name="6")

    assert a == b
    assert a != c
    assert b != c

    assert hash(a) == hash(b)
    assert hash(a) != hash(c)
    assert hash(b) != hash(c)


def test_object_identifier_from_kopf_core_resource() -> None:
    resource = kopf.Resource(group="", version="v1", plural="pods")
    oid = ObjectIdentifier(namespace="default", resource=resource, name="foo")
    assert oid.namespace == "default"
    assert oid.resource == "pods.v1"
    assert oid.name == "foo"


def test_object_identifier_from_kopf_resource() -> None:
    resource = kopf.Resource(group="storage.k8s.io", version="v1", plural="csidrivers")
    oid = ObjectIdentifier(namespace="default", resource=resource, name="bar")
    assert oid.namespace == "default"
    assert oid.resource == "csidrivers.v1.storage.k8s.io"
    assert oid.name == "bar"
