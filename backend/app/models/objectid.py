"""Helpers for MongoDB ObjectId with Pydantic v2."""
from __future__ import annotations

from typing import Any

from bson import ObjectId


def coerce_object_id(v: Any) -> ObjectId | None:
    if v is None:
        return None
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str) and ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")
