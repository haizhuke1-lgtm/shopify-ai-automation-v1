"""Structured pipeline logging and tracking utilities."""

from __future__ import annotations

from typing import Any

from src.core.schema import utc_now_iso


class PipelineLogger:
    """Collect timestamped success/failure events for each pipeline module."""

    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def track(self, stage: str, module: str, status: str, message: str = "", **metadata: Any) -> None:
        self.events.append(
            {
                "timestamp": utc_now_iso(),
                "stage": stage,
                "module": module,
                "status": status,
                "message": message,
                "metadata": metadata,
            }
        )

    def success(self, stage: str, module: str, message: str = "", **metadata: Any) -> None:
        self.track(stage, module, "success", message, **metadata)

    def failure(self, stage: str, module: str, message: str = "", **metadata: Any) -> None:
        self.track(stage, module, "failure", message, **metadata)
