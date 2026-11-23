"""Starter for the vLLM-HUST preemption-policy v1 contract."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vllm.v1.core.sched.preemption import PreemptionContext


class PreemptionPolicy:
    vllm_preemption_policy_api_version = 1

    def select_victim(self, context: PreemptionContext) -> str | None:
        """Return a candidate ID, or delegate to the host by returning None."""
        # Implement your policy using the read-only context and its candidates.
        return None
