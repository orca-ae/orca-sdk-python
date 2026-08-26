# API surface

Every public method on the client, generated from the code itself so this file
cannot drift from what ships. Each maps 1:1 to an `operationId` in the vendored
contract; `tests/test_contract.py` enforces that.

## `client.agents`

| Method | Returns |
|---|---|
| `client.agents.archive()` | `Agent` |
| `client.agents.create()` | `Agent` |
| `client.agents.list()` | `SyncPageCursor[Agent]` |
| `client.agents.retrieve()` | `Agent` |
| `client.agents.update()` | `Agent` |
| `client.agents.versions.list()` | `SyncPageCursor[Agent]` |

## `client.sessions`

| Method | Returns |
|---|---|
| `client.sessions.archive()` | `Session` |
| `client.sessions.create()` | `Session` |
| `client.sessions.delete()` | `DeletedSession` |
| `client.sessions.list()` | `SyncPageCursor[Session]` |
| `client.sessions.retrieve()` | `Session` |
| `client.sessions.update()` | `Session` |
| `client.sessions.events.list()` | `SyncPageCursor[SessionEvent]` |
| `client.sessions.events.send()` | `SessionEventSendResponse` |
| `client.sessions.events.stream()` | `Stream[SessionEvent]` |
| `client.sessions.files.delete()` | `DeletedSessionFile` |
| `client.sessions.files.download()` | `httpx2.Response` |
| `client.sessions.files.list()` | `SyncPage[SessionFile]` |
| `client.sessions.files.retrieve()` | `SessionFile` |
| `client.sessions.resources.add()` | `SessionResource` |
| `client.sessions.resources.delete()` | `DeletedSessionResource` |
| `client.sessions.resources.list()` | `SyncPageCursor[SessionResource]` |
| `client.sessions.resources.retrieve()` | `SessionResource` |
| `client.sessions.resources.update()` | `SessionResource` |
| `client.sessions.threads.archive()` | `SessionThread` |
| `client.sessions.threads.list()` | `SyncPageCursor[SessionThread]` |
| `client.sessions.threads.retrieve()` | `SessionThread` |
| `client.sessions.threads.events.list()` | `SyncPageCursor[SessionEvent]` |
| `client.sessions.threads.events.stream()` | `Stream[SessionEvent]` |

## `client.environments`

| Method | Returns |
|---|---|
| `client.environments.archive()` | `Environment` |
| `client.environments.create()` | `Environment` |
| `client.environments.delete()` | `DeletedEnvironment` |
| `client.environments.list()` | `SyncPageCursor[Environment]` |
| `client.environments.retrieve()` | `Environment` |
| `client.environments.update()` | `Environment` |

## `client.files`

| Method | Returns |
|---|---|
| `client.files.delete()` | `DeletedFile` |
| `client.files.download()` | `httpx2.Response` |
| `client.files.list()` | `SyncPage[FileMetadata]` |
| `client.files.retrieve()` | `FileMetadata` |
| `client.files.upload()` | `FileMetadata` |

## `client.skills`

| Method | Returns |
|---|---|
| `client.skills.create()` | `Skill` |
| `client.skills.delete()` | `DeletedSkill` |
| `client.skills.list()` | `SyncPageCursor[Skill]` |
| `client.skills.retrieve()` | `Skill` |
| `client.skills.versions.create()` | `SkillVersion` |
| `client.skills.versions.delete()` | `DeletedSkillVersion` |
| `client.skills.versions.list()` | `SyncPageCursor[SkillVersion]` |
| `client.skills.versions.retrieve()` | `SkillVersion` |

## `client.vaults`

| Method | Returns |
|---|---|
| `client.vaults.archive()` | `Vault` |
| `client.vaults.create()` | `Vault` |
| `client.vaults.delete()` | `DeletedVault` |
| `client.vaults.list()` | `SyncPageCursor[Vault]` |
| `client.vaults.retrieve()` | `Vault` |
| `client.vaults.update()` | `Vault` |
| `client.vaults.credentials.archive()` | `VaultCredential` |
| `client.vaults.credentials.create()` | `VaultCredential` |
| `client.vaults.credentials.delete()` | `DeletedVaultCredential` |
| `client.vaults.credentials.list()` | `SyncPageCursor[VaultCredential]` |
| `client.vaults.credentials.retrieve()` | `VaultCredential` |
| `client.vaults.credentials.update()` | `VaultCredential` |
| `client.vaults.credentials.validate()` | `CredentialValidation` |

## `client.memory_stores`

| Method | Returns |
|---|---|
| `client.memory_stores.archive()` | `MemoryStore` |
| `client.memory_stores.create()` | `MemoryStore` |
| `client.memory_stores.delete()` | `DeletedMemoryStore` |
| `client.memory_stores.list()` | `SyncPageCursor[MemoryStore]` |
| `client.memory_stores.retrieve()` | `MemoryStore` |
| `client.memory_stores.update()` | `MemoryStore` |
| `client.memory_stores.memories.create()` | `Memory` |
| `client.memory_stores.memories.delete()` | `DeletedMemory` |
| `client.memory_stores.memories.list()` | `SyncPageCursor[MemoryListItem]` |
| `client.memory_stores.memories.retrieve()` | `Memory` |
| `client.memory_stores.memories.update()` | `Memory` |
| `client.memory_stores.memory_versions.list()` | `SyncPageCursor[MemoryVersion]` |
| `client.memory_stores.memory_versions.redact()` | `MemoryVersion` |
| `client.memory_stores.memory_versions.retrieve()` | `MemoryVersion` |

## `client.triggers`

| Method | Returns |
|---|---|
| `client.triggers.create()` | `Trigger` |
| `client.triggers.delete()` | `DeletedTrigger` |
| `client.triggers.list()` | `SyncPageCursor[Trigger]` |
| `client.triggers.pause()` | `Trigger` |
| `client.triggers.retrieve()` | `Trigger` |
| `client.triggers.unpause()` | `Trigger` |
| `client.triggers.update()` | `Trigger` |
| `client.triggers.sessions.list()` | `SyncPageCursor[object]` |

## `client.discovery`

| Method | Returns |
|---|---|
| `client.discovery.groups()` | `APIGroupList` |

## `client.cloud`

| Method | Returns |
|---|---|
| `client.cloud.agents.providers.list()` | `CloudAgentProviderList` |
| `client.cloud.agents.providers.retrieve()` | `CloudAgentProvider` |
| `client.cloud.api_resources.list()` | `CloudAPIResourceList` |
| `client.cloud.catalog.kafka.list()` | `CloudCatalogConnectorList` |
| `client.cloud.catalog.kafka.retrieve()` | `CloudCatalogConfigFieldList` |
| `client.cloud.catalog.sinks.list()` | `CloudCatalogConnectorList` |
| `client.cloud.catalog.sinks.retrieve()` | `CloudCatalogConfigFieldList` |
| `client.cloud.catalog.sources.list()` | `CloudCatalogConnectorList` |
| `client.cloud.catalog.sources.retrieve()` | `CloudCatalogConfigFieldList` |
| `client.cloud.connections.create()` | `object` |
| `client.cloud.connections.delete()` | `object` |
| `client.cloud.connections.list()` | `List[CloudConnection]` |
| `client.cloud.connections.retrieve()` | `CloudConnection` |
| `client.cloud.connections.test()` | `CloudConnectionHealth` |
| `client.cloud.connections.update()` | `object` |
| `client.cloud.connections.validate()` | `object` |
| `client.cloud.connectors.kafka.health()` | `CloudKafkaWorkerStatus` |
| `client.cloud.connectors.kafka.server_info()` | `CloudKafkaServerInfo` |
| `client.cloud.connectors.kafka.connectors.create()` | `CloudKafkaConnectorInfo` |
| `client.cloud.connectors.kafka.connectors.delete()` | `object` |
| `client.cloud.connectors.kafka.connectors.list()` | `CloudKafkaOpenResponse` |
| `client.cloud.connectors.kafka.connectors.list_tasks()` | `CloudKafkaTaskInfoList` |
| `client.cloud.connectors.kafka.connectors.pause()` | `object` |
| `client.cloud.connectors.kafka.connectors.reset_active_topics()` | `object` |
| `client.cloud.connectors.kafka.connectors.reset_offsets()` | `CloudKafkaMessage` |
| `client.cloud.connectors.kafka.connectors.restart()` | `object` |
| `client.cloud.connectors.kafka.connectors.restart_task()` | `object` |
| `client.cloud.connectors.kafka.connectors.resume()` | `object` |
| `client.cloud.connectors.kafka.connectors.retrieve()` | `CloudKafkaConnectorInfo` |
| `client.cloud.connectors.kafka.connectors.retrieve_active_topics()` | `CloudKafkaOpenResponse` |
| `client.cloud.connectors.kafka.connectors.retrieve_config()` | `CloudKafkaOpenResponse` |
| `client.cloud.connectors.kafka.connectors.retrieve_offsets()` | `CloudKafkaConnectorOffsets` |
| `client.cloud.connectors.kafka.connectors.retrieve_status()` | `CloudKafkaConnectorStateInfo` |
| `client.cloud.connectors.kafka.connectors.retrieve_task_status()` | `CloudKafkaTaskState` |
| `client.cloud.connectors.kafka.connectors.retrieve_tasks_config()` | `CloudKafkaOpenResponse` |
| `client.cloud.connectors.kafka.connectors.stop()` | `object` |
| `client.cloud.connectors.kafka.connectors.update_config()` | `CloudKafkaConnectorInfo` |
| `client.cloud.connectors.kafka.connectors.update_offsets()` | `CloudKafkaMessage` |
| `client.cloud.connectors.kafka.plugins.list()` | `CloudKafkaPluginInfoList` |
| `client.cloud.connectors.kafka.plugins.list_catalog()` | `CloudKafkaPluginCatalogEntryList` |
| `client.cloud.connectors.kafka.plugins.retrieve_config()` | `CloudKafkaConfigKeyInfoList` |
| `client.cloud.connectors.sinks.create()` | `object` |
| `client.cloud.connectors.sinks.delete()` | `object` |
| `client.cloud.connectors.sinks.list()` | `CloudSinkNameList` |
| `client.cloud.connectors.sinks.restart()` | `object` |
| `client.cloud.connectors.sinks.restart_instance()` | `object` |
| `client.cloud.connectors.sinks.retrieve()` | `CloudSinkConfig` |
| `client.cloud.connectors.sinks.retrieve_instance_status()` | `CloudSinkInstanceStatus` |
| `client.cloud.connectors.sinks.retrieve_status()` | `CloudSinkStatus` |
| `client.cloud.connectors.sinks.start()` | `object` |
| `client.cloud.connectors.sinks.start_instance()` | `object` |
| `client.cloud.connectors.sinks.stop()` | `object` |
| `client.cloud.connectors.sinks.stop_instance()` | `object` |
| `client.cloud.connectors.sinks.update()` | `object` |
| `client.cloud.connectors.sources.create()` | `object` |
| `client.cloud.connectors.sources.delete()` | `object` |
| `client.cloud.connectors.sources.list()` | `CloudSourceNameList` |
| `client.cloud.connectors.sources.restart()` | `object` |
| `client.cloud.connectors.sources.restart_instance()` | `object` |
| `client.cloud.connectors.sources.retrieve()` | `CloudSourceConfig` |
| `client.cloud.connectors.sources.retrieve_instance_status()` | `CloudSourceInstanceStatus` |
| `client.cloud.connectors.sources.retrieve_status()` | `CloudSourceStatus` |
| `client.cloud.connectors.sources.start()` | `object` |
| `client.cloud.connectors.sources.start_instance()` | `object` |
| `client.cloud.connectors.sources.stop()` | `object` |
| `client.cloud.connectors.sources.stop_instance()` | `object` |
| `client.cloud.connectors.sources.update()` | `object` |
| `client.cloud.functions.create()` | `object` |
| `client.cloud.functions.delete()` | `object` |
| `client.cloud.functions.list()` | `List[str]` |
| `client.cloud.functions.restart()` | `object` |
| `client.cloud.functions.restart_instance()` | `object` |
| `client.cloud.functions.retrieve()` | `CloudFunctionConfig` |
| `client.cloud.functions.retrieve_instance_stats()` | `CloudFunctionInstanceStats` |
| `client.cloud.functions.retrieve_instance_status()` | `CloudFunctionInstanceStatus` |
| `client.cloud.functions.retrieve_state()` | `CloudFunctionState` |
| `client.cloud.functions.retrieve_stats()` | `CloudFunctionStats` |
| `client.cloud.functions.retrieve_status()` | `CloudFunctionStatus` |
| `client.cloud.functions.start()` | `object` |
| `client.cloud.functions.start_instance()` | `object` |
| `client.cloud.functions.stop()` | `object` |
| `client.cloud.functions.stop_instance()` | `object` |
| `client.cloud.functions.trigger()` | `str` |
| `client.cloud.functions.update()` | `object` |
| `client.cloud.functions.update_state()` | `object` |
| `client.cloud.health.check()` | `bool` |
| `client.cloud.health.live()` | `bool` |
| `client.cloud.health.ready()` | `bool` |
| `client.cloud.packages.delete()` | `object` |
| `client.cloud.packages.download()` | `httpx2.Response` |
| `client.cloud.packages.list()` | `object` |
| `client.cloud.packages.list_versions()` | `object` |
| `client.cloud.packages.retrieve_metadata()` | `object` |
| `client.cloud.packages.update_metadata()` | `object` |
| `client.cloud.packages.upload()` | `object` |

---

**179 public methods.** Each is available on both `Orca` and `AsyncOrca`,
with the same signature, plus `.with_raw_response` and `.with_streaming_response`
variants.
