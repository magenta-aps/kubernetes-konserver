# SPDX-FileCopyrightText: 2022 Magenta ApS
# SPDX-License-Identifier: MPL-2.0
from typing import Any

import kopf

from . import util
from .config import config
from .models import ObjectIdentifier


@kopf.on.startup()
async def configure(settings: kopf.OperatorSettings, **_: Any) -> None:
    """Startup event handler.

    Args:
        settings: Kopf settings to modify.
        **_: Required for kopf forward compatibility.

    Returns: None.
    """
    # Override the name of the finalizer added to objects
    settings.persistence.finalizer = config.annotation.internal_finalizer

    # Override the prefixes used for persistence annotations added to objects.
    settings.persistence.progress_storage = kopf.AnnotationsProgressStorage(
        prefix=config.annotation.internal_prefix
    )
    settings.persistence.diffbase_storage = kopf.AnnotationsDiffBaseStorage(
        prefix=config.annotation.internal_prefix
    )


@util.multi_handler(
    kopf.index,
    config.watched_resources,
    annotations={config.annotation.conserve: kopf.PRESENT},
)
async def conservations(
    name: str,
    namespace: str,
    resource: kopf.Resource,
    annotations: dict[str, str],
    **_: Any,
) -> dict[ObjectIdentifier, ObjectIdentifier]:
    """Maintain in-memory index of object conservations.

    Args:
        name: Name of the conservator object.
        namespace: Namespace of the conservator object.
        resource: Resource type of the conservator object.
        annotations: Annotations on the conservator object.
        **_: Required for kopf forward compatibility.

    Returns: Dictionary to merge into the index.
    """
    conservator = ObjectIdentifier(namespace=namespace, resource=resource, name=name)
    conserved_objects = util.parse_conserves(
        namespace, annotations[config.annotation.conserve]
    )
    return dict.fromkeys(conserved_objects, conservator)


@util.multi_handler(
    kopf.on.delete,
    config.watched_resources,
    annotations={config.annotation.conservable: "yes"},
)
async def conserve(
    name: str,
    namespace: str,
    resource: kopf.Resource,
    conservations: kopf.Index,
    **_: Any,
) -> None:
    """Conserve object from deletion.

    Args:
        name: Name of the (possibly) conserved object.
        namespace: Namespace of the (possibly) conserved object.
        resource: Resource type of the (possibly) conserved object.
        conservations: In-memory overview of conservations.
        **_: Required for kopf forward compatibility.

    Raises: TemporaryError, blocking deletion, if object is to be conserved.
    """
    obj = ObjectIdentifier(namespace=namespace, resource=resource, name=name)
    if conservators := conservations.get(obj):
        raise kopf.TemporaryError(
            f"Deletion of {resource} conserved by: {conservators}"
        )
