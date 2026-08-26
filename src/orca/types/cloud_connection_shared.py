"""Request shapes for `client.cloud.connections`.

Field names here are the wire names verbatim. The cloud extension serves
camelCase JSON, and `AGENTS.md` §5 says we mirror the wire shape rather than
re-spell it, so `bootstrapServers` stays `bootstrapServers`. Only names that
are not valid Python identifiers get an alias.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

__all__ = [
    "CloudConnectionSpecParam",
    "CloudConnectionSecretRefParam",
    "CloudConnectionGenericAuthParam",
    "CloudConnectionOAuth2Param",
    "CloudKafkaConnectionParam",
    "CloudOtherConnectionParam",
    "CloudPulsarConnectionParam",
    "CloudConnectionTypeParam",
]

CloudConnectionTypeParam: TypeAlias = Literal["pulsar", "kafka", "other"]


class CloudConnectionSecretRefParam(TypedDict, total=False):
    key: str

    name: str


class CloudConnectionGenericAuthParam(TypedDict, total=False):
    clientAuthenticationParameters: str

    clientAuthenticationPlugin: str


class CloudConnectionOAuth2Param(TypedDict, total=False):
    audience: str

    issuerUrl: str

    keySecretKey: str

    keySecretName: str

    scope: Optional[str]


class CloudKafkaPlainAuthParam(TypedDict, total=False):
    passwordKey: Optional[str]

    secretName: str

    usernameKey: Optional[str]


class CloudKafkaScramAuthParam(CloudKafkaPlainAuthParam, total=False):
    hashAlgorithm: Optional[Literal["SHA-256", "SHA-512"]]


class CloudKafkaConnectionAuthenticationParam(TypedDict, total=False):
    genericAuth: Optional[CloudConnectionGenericAuthParam]

    oauth2Config: Optional[CloudConnectionOAuth2Param]

    plainAuthConfig: Optional[CloudKafkaPlainAuthParam]

    scramAuthConfig: Optional[CloudKafkaScramAuthParam]


class CloudKafkaKeyStoreConfigParam(TypedDict, total=False):
    fileKey: Optional[str]

    keyPasswordKey: Optional[str]

    passwordKey: Optional[str]

    secretName: Optional[str]

    type: Optional[Literal["JKS", "PEM", "PKCS12"]]


class CloudKafkaTrustStoreConfigParam(TypedDict, total=False):
    fileKey: Optional[str]

    passwordKey: Optional[str]

    secretName: Optional[str]

    type: Optional[Literal["JKS", "PEM", "PKCS12"]]


class CloudKafkaConnectionTLSParam(TypedDict, total=False):
    enabled: Optional[bool]

    keyStoreConfig: Optional[CloudKafkaKeyStoreConfigParam]

    trustStoreConfig: Optional[CloudKafkaTrustStoreConfigParam]


class CloudKafkaConnectionParam(TypedDict, total=False):
    authentication: Optional[CloudKafkaConnectionAuthenticationParam]

    bootstrapServers: str

    tls: Optional[CloudKafkaConnectionTLSParam]


class CloudOtherConnectionParam(TypedDict, total=False):
    endpoint: str

    properties: Optional[Dict[str, str]]

    secretRef: Optional[CloudConnectionSecretRefParam]


class CloudPulsarConnectionAuthenticationParam(TypedDict, total=False):
    genericAuth: Optional[CloudConnectionGenericAuthParam]

    oauth2: Optional[CloudConnectionOAuth2Param]

    token: Optional[CloudConnectionSecretRefParam]


class CloudPulsarConnectionTLSParam(TypedDict, total=False):
    allowInsecureConnection: Optional[bool]

    clientCertSecretRef: Optional[CloudConnectionSecretRefParam]

    clientKeySecretRef: Optional[CloudConnectionSecretRefParam]

    enableHostnameVerification: Optional[bool]

    enabled: Optional[bool]

    trustCertsSecretRef: Optional[CloudConnectionSecretRefParam]


class CloudPulsarConnectionParam(TypedDict, total=False):
    adminUrl: Optional[str]

    authentication: Optional[CloudPulsarConnectionAuthenticationParam]

    serviceUrl: str

    tls: Optional[CloudPulsarConnectionTLSParam]


class CloudConnectionStatusConditionParam(TypedDict, total=False):
    lastTransitionTime: str

    message: str

    observedGeneration: Optional[int]

    reason: str

    status: Literal["True", "False", "Unknown"]

    type: str


class CloudConnectionStatusParam(TypedDict, total=False):
    """Server-owned status.

    The contract accepts it on writes because create/update/validate all take the
    whole connection document, but the server derives it -- sending one has no
    effect beyond round-tripping a value you read earlier.
    """

    conditions: Optional[List[CloudConnectionStatusConditionParam]]

    lastTestedAt: Optional[str]

    message: Optional[str]

    observedGeneration: Optional[int]

    phase: Optional[Literal["Unknown", "Healthy", "Unhealthy", "Testing"]]


class CloudConnectionSpecParam(TypedDict, total=False):
    kafka: Optional[CloudKafkaConnectionParam]

    other: Optional[CloudOtherConnectionParam]

    pulsar: Optional[CloudPulsarConnectionParam]

    type: CloudConnectionTypeParam
