from __future__ import annotations

SCHEMA_VERSION = "weslr_arc_agi2_public_submission_v1"
DUMMY_SOURCE_KIND = "dummy_no_data_fixture_v1"
ALLOWED_PACKET_KEYS = (
    "task_id",
    "anonymized_task_id",
    "train_pairs",
    "test_inputs",
    "required_output_count",
    "format_metadata",
    "parse_status",
    "source_kind",
    "packet_metadata",
)
