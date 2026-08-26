from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "CloudConnection",
    "CloudConnectionListResponse",
    "CloudConnectionHealth",
    "CloudConnectionSpec",
    "CloudConnectionStatus",
    "CloudConnectionSecretRef",
    "CloudConnectionGenericAuth",
    "CloudConnectionOAuth2",
    "CloudKafkaConnection",
    "CloudOtherConnection",
    "CloudPulsarConnection",
    "CloudConnectionStatusCondition",
]


class CloudConnectionSecretRef(BaseModel):
    key: Optional[str] = None

    name: Optional[str] = None


class CloudConnectionGenericAuth(BaseModel):
    clientAuthenticationParameters: Optional[str] = None

    clientAuthenticationPlugin: Optional[str] = None


class CloudConnectionOAuth2(BaseModel):
    audience: Optional[str] = None

    issuerUrl: Optional[str] = None

    keySecretKey: Optional[str] = None

    keySecretName: Optional[str] = None

    scope: Optional[str] = None


class CloudKafkaPlainAuth(BaseModel):
    passwordKey: Optional[str] = None

    secretName: Optional[str] = None

    usernameKey: Optional[str] = None


class CloudKafkaScramAuth(CloudKafkaPlainAuth):
    hashAlgorithm: Optional[Literal["SHA-256", "SHA-512"]] = None


class CloudKafkaConnectionAuthentication(BaseModel):
    genericAuth: Optional[CloudConnectionGenericAuth] = None

    oauth2Config: Optional[CloudConnectionOAuth2] = None

    plainAuthConfig: Optional[CloudKafkaPlainAuth] = None

    scramAuthConfig: Optional[CloudKafkaScramAuth] = None


class CloudKafkaKeyStoreConfig(BaseModel):
    fileKey: Optional[str] = None

    keyPasswordKey: Optional[str] = None

    passwordKey: Optional[str] = None

    secretName: Optional[str] = None

    type: Optional[Literal["JKS", "PEM", "PKCS12"]] = None


class CloudKafkaTrustStoreConfig(BaseModel):
    fileKey: Optional[str] = None

    passwordKey: Optional[str] = None

    secretName: Optional[str] = None

    type: Optional[Literal["JKS", "PEM", "PKCS12"]] = None


class CloudKafkaConnectionTLS(BaseModel):
    enabled: Optional[bool] = None

    keyStoreConfig: Optional[CloudKafkaKeyStoreConfig] = None

    trustStoreConfig: Optional[CloudKafkaTrustStoreConfig] = None


class CloudKafkaConnection(BaseModel):
    authentication: Optional[CloudKafkaConnectionAuthentication] = None

    bootstrapServers: Optional[str] = None

    tls: Optional[CloudKafkaConnectionTLS] = None


class CloudOtherConnection(BaseModel):
    endpoint: Optional[str] = None

    properties: Optional[Dict[str, str]] = None

    secretRef: Optional[CloudConnectionSecretRef] = None


class CloudPulsarConnectionAuthentication(BaseModel):
    genericAuth: Optional[CloudConnectionGenericAuth] = None

    oauth2: Optional[CloudConnectionOAuth2] = None

    token: Optional[CloudConnectionSecretRef] = None


class CloudPulsarConnectionTLS(BaseModel):
    allowInsecureConnection: Optional[bool] = None

    clientCertSecretRef: Optional[CloudConnectionSecretRef] = None

    clientKeySecretRef: Optional[CloudConnectionSecretRef] = None

    enableHostnameVerification: Optional[bool] = None

    enabled: Optional[bool] = None

    trustCertsSecretRef: Optional[CloudConnectionSecretRef] = None


class CloudPulsarConnection(BaseModel):
    adminUrl: Optional[str] = None

    authentication: Optional[CloudPulsarConnectionAuthentication] = None

    serviceUrl: Optional[str] = None

    tls: Optional[CloudPulsarConnectionTLS] = None


class CloudConnectionSpec(BaseModel):
    kafka: Optional[CloudKafkaConnection] = None

    other: Optional[CloudOtherConnection] = None

    pulsar: Optional[CloudPulsarConnection] = None

    type: Optional[Literal["pulsar", "kafka", "other"]] = None


class CloudConnectionStatusCondition(BaseModel):
    lastTransitionTime: Optional[str] = None

    message: Optional[str] = None

    observedGeneration: Optional[int] = None

    reason: Optional[str] = None

    status: Optional[Literal["True", "False", "Unknown"]] = None

    type: Optional[str] = None


class CloudConnectionStatus(BaseModel):
    conditions: Optional[List[CloudConnectionStatusCondition]] = None

    lastTestedAt: Optional[str] = None

    message: Optional[str] = None

    observedGeneration: Optional[int] = None

    phase: Optional[Literal["Unknown", "Healthy", "Unhealthy", "Testing"]] = None


class CloudConnection(BaseModel):
    """A stored external connection.

    Every field is optional: the contract declares no required properties, and
    `status` is server-owned -- it is echoed back on reads and ignored on writes.
    """

    name: Optional[str] = None

    spec: Optional[CloudConnectionSpec] = None

    status: Optional[CloudConnectionStatus] = None

    internal: Optional[bool] = None

    clusterRef: Optional[str] = None


class CloudConnectionHealth(BaseModel):
    """The result of testing a stored connection."""

    name: Optional[str] = None

    phase: Optional[str] = None

    healthy: Optional[bool] = None

    message: Optional[str] = None

    lastTestedAt: Optional[str] = None


CloudConnectionListResponse: TypeAlias = List[CloudConnection]
