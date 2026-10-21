"""Interfaces for future verified game adapters. No synthetic implementation."""
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class GameIdentity:
    slug: str
    version: str


@dataclass(frozen=True)
class RuntimeEvidence:
    system_id: str
    host: GameIdentity
    companion: GameIdentity
    report_path: str
    report_sha256: str


class HostAdapter(Protocol):
    """Must operate inside the real ZZZ workflow through a supported route."""
    def identity(self) -> GameIdentity: ...
    def verify_runtime(self) -> RuntimeEvidence: ...


class CompanionAdapter(Protocol):
    """Must supply actual permitted Fortnite content/gameplay provenance."""
    def identity(self) -> GameIdentity: ...
    def verify_runtime(self) -> RuntimeEvidence: ...


def require_runtime():
    raise RuntimeError('Blocked: no verified ZZZ host or Fortnite companion adapter exists')
