from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AccountSummary:
    username: str
    tag: Optional[str]
    status: str
    videos_uploaded: int


@dataclass(frozen=True)
class UploadOutcome:
    username: str
    video_path: str
    status: str
    error: Optional[str] = None
    created_at: Optional[str] = None


@dataclass(frozen=True)
class UploadRunSummary:
    total: int
    succeeded: int
    failed: int
    stopped: bool
    outcomes: tuple[UploadOutcome, ...]
