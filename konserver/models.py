# SPDX-FileCopyrightText: 2022 Magenta ApS
# SPDX-License-Identifier: MPL-2.0
from typing import Any

import kopf
from pydantic import BaseModel
from pydantic import validator


class Resource(BaseModel):
    """Kubernetes resource identifier"""

    group: str
    version: str
    name: str


class ObjectIdentifier(BaseModel):
    """Identifier of a named kubernetes object."""

    namespace: str
    resource: str
    name: str

    class Config:
        frozen = True

    @validator("resource", pre=True)
    def convert_from_kopf_resource(cls, value: Any) -> Any:
        """Allow passing kopf Resource instead of string."""
        if isinstance(value, kopf.Resource):
            return repr(value)
        return value
