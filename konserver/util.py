# SPDX-FileCopyrightText: 2022 Magenta ApS
# SPDX-License-Identifier: MPL-2.0
from collections.abc import Callable
from collections.abc import Iterable
from typing import Any

from .models import ObjectIdentifier
from .models import Resource


def parse_conserves(namespace: str, conserves: str | None) -> list[ObjectIdentifier]:
    """Parse annotation of conserves into object identifiers.

    Args:
        namespace: Namespace of the conservator object.
        conserves: Comma-separated string of conserved objects.

    Returns: List of identifiers for conserved objects.
    """
    if conserves is None:
        return []

    def construct_identifier(conserve: str) -> ObjectIdentifier:
        resource, name = conserve.rsplit("/", maxsplit=1)
        return ObjectIdentifier(namespace=namespace, resource=resource, name=name)

    return list(map(construct_identifier, conserves.split(",")))


def multi_handler(
    kopf_decorator: Callable, resources: Iterable[Resource], **kwargs: Any
) -> Callable:
    """Register kopf handler for multiple resource types.

    Args:
        kopf_decorator: Kopf event handler decorator function.
        resources: Iterator of resource type specifications.
        **kwargs: Additional kwargs passed to each kopf handler decorator.

    Returns: Decorator.
    """

    def decorator(f: Callable) -> Callable:
        for resource in resources:
            f = kopf_decorator(
                resource.group, resource.version, resource.name, **kwargs
            )(f)
        return f

    return decorator
