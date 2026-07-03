from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .schema import DUMMY_SOURCE_KIND, SCHEMA_VERSION

FIXTURE_NAME = "arc_official_public_dummy_no_data_v1.json"
FIXTURE_PATH = Path("tests/fixtures/dummy_no_data") / FIXTURE_NAME


def build_dummy_approval_manifest(source_version_or_snapshot: str = "dummy-no-data-v1") -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "owner_approved": True,
        "approval_reference": "dummy-public-parse-scorer-0001",
        "approved_phase": "phase_2_public_parse_scorer_validation",
        "source_kind": DUMMY_SOURCE_KIND,
        "source_location": str(FIXTURE_PATH),
        "source_version_or_snapshot": source_version_or_snapshot,
        "checksum": None,
        "dummy_no_data": True,
        "claim_policy": {
            "official_score_claimable": False,
            "official_percentage_claimable": "none/0",
            "synthetic_official_score_mixing": False,
            "competition_submission_authority": False,
        },
        "approved_scope": {"fixture_only": True, "scope": "dummy-no-data-public-surface"},
    }


def validate_dummy_approval_manifest(manifest: Any) -> dict[str, Any]:
    data = manifest if isinstance(manifest, Mapping) else {}
    if not data:
        raise ValueError("approval manifest required")
    issues: list[str] = []
    if data.get("owner_approved") is not True:
        issues.append("owner_not_approved")
    if str(data.get("source_kind", "")) != DUMMY_SOURCE_KIND:
        issues.append("source_kind_mismatch")
    if str(data.get("source_location", "")) != str(FIXTURE_PATH):
        issues.append("source_location_mismatch")
    if data.get("dummy_no_data") is not True:
        issues.append("missing_dummy_no_data_marker")
    claim_policy = data.get("claim_policy") if isinstance(data.get("claim_policy"), Mapping) else {}
    if claim_policy.get("official_score_claimable") is not False:
        issues.append("official_score_claimable_must_be_false")
    if str(claim_policy.get("official_percentage_claimable", "")).lower() not in {"none/0", "none", "0"}:
        issues.append("official_percentage_claimable_must_remain_none_zero")
    if issues:
        raise ValueError(f"Invalid approval manifest: {sorted(set(issues))}")
    return {"valid": True, "source_location": str(FIXTURE_PATH), "dummy_no_data": True}
