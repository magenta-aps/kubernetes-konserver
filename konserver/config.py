# SPDX-FileCopyrightText: 2022 Magenta ApS
# SPDX-License-Identifier: MPL-2.0
from pydantic import BaseModel
from pydantic import BaseSettings

from konserver.models import Resource


class Annotation(BaseModel):
    prefix: str = "konserver.magenta.dk"

    internal_prefix: str = f"internal.{prefix}"
    internal_finalizer: str = f"{internal_prefix}/finalizer"

    conservable: str = f"{prefix}/conservable"
    conserve: str = f"{prefix}/conserve"

    # @root_validator
    # Note that this prefix MUST be different from the ones we use in our
    # handlers, or events will be ignored.
    # def check_passwords_match(cls, values):
    #     """"""
    #     pw1, pw2 = values.get('password1'), values.get('password2')
    #     if pw1 is not None and pw2 is not None and pw1 != pw2:
    #         raise ValueError('passwords do not match')
    #     return values


class Config(BaseSettings):
    watched_resources: list[Resource] = [
        # Default to all namespaced core v1 resources
        Resource(group="", version="v1", name="configmaps"),
        Resource(group="", version="v1", name="endpoints"),
        Resource(group="", version="v1", name="events"),
        Resource(group="", version="v1", name="limitranges"),
        Resource(group="", version="v1", name="namespaces"),
        Resource(group="", version="v1", name="persistentvolumeclaims"),
        Resource(group="", version="v1", name="pods"),
        Resource(group="", version="v1", name="podtemplates"),
        Resource(group="", version="v1", name="replicationcontrollers"),
        Resource(group="", version="v1", name="resourcequotas"),
        Resource(group="", version="v1", name="secrets"),
        Resource(group="", version="v1", name="serviceaccounts"),
        Resource(group="", version="v1", name="services"),
    ]
    annotation: Annotation = Annotation()

    class Config:
        env_nested_delimiter = "__"  # allows setting e.g. ANNOTATION_PREFIX=foo


config = Config()
