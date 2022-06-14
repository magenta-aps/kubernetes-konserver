# SPDX-FileCopyrightText: 2022 Magenta ApS
# SPDX-License-Identifier: MPL-2.0
import kopf
import pytest

from konserver.main import conservations
from konserver.main import conserve
from konserver.models import ObjectIdentifier


async def test_conservations_index() -> None:
    # The conservations index function is called with the conservator object,
    # i.e. the object with the 'konserver.magenta.dk/conserve' annotation.
    ns = "default"
    conservator = ObjectIdentifier(namespace=ns, resource="secrets.v1", name="con")

    actual = await conservations(
        name=conservator.name,
        namespace=ns,
        resource=kopf.Resource(group="", version="v1", plural="secrets"),
        annotations={
            "unrelated": "foo",
            "konserver.magenta.dk/conserve": "configmaps.v1/foo,pods.v1/bar",
        },
    )

    # We expect the function to parse the annotation and return a dictionary
    # containing the conserved objects and their conservator.
    expected = {
        ObjectIdentifier(
            namespace=ns, resource="configmaps.v1", name="foo"
        ): conservator,
        ObjectIdentifier(namespace=ns, resource="pods.v1", name="bar"): conservator,
    }
    assert actual == expected


async def test_conserve_deletion_handler() -> None:
    conservations_index: dict = {}
    actual = await conserve(
        name="foo",
        namespace="default",
        resource=kopf.Resource(group="", version="v1", plural="pods"),
        conservations=conservations_index,  # type: ignore
    )
    assert actual is None


async def test_conserve_deletion_handler_raises() -> None:
    ns = "default"
    conservations_index = {
        ObjectIdentifier(namespace=ns, resource="pods.v1", name="foo"): ["bar"]
    }
    with pytest.raises(kopf.TemporaryError):
        await conserve(
            name="foo",
            namespace=ns,
            resource=kopf.Resource(group="", version="v1", plural="pods"),
            conservations=conservations_index,  # type: ignore
        )
