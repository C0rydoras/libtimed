import typing as t


class BaseRecord(t.TypedDict):
    """Record that contains only id and type."""

    id: str
    type: str


class Record(BaseRecord):
    """Record with attributes and relationships."""

    attributes: dict[str, t.Any] | None
    relationships: dict[str, BaseRecord] | None


T = t.TypeVar("T", list[Record], Record)


class Data(t.TypedDict):
    """JSON:API Response."""

    data: T
    included: list[Record] | None


class DeserializationError(Exception):
    """Raised when deserialization fails."""


class MissingKeyError(DeserializationError):
    """Raised when theres a missing key when deserializing."""

    def __init__(self, key: str, *args):
        message = f"Missing required key: {key}"
        super().__init__(message, *args)


class ForbiddenKeyError(DeserializationError):
    """Raised when theres a forbidden key when deserializing."""

    def __init__(self, key: str, *args):
        message = f"Forbidden key used: {key}"
        super().__init__(message, *args)


def deserialize_record(record: Record, included: list[Record]):
    """Deserialize single record into human readable value."""
    attributes = record.get("attributes", {})
    relationships = record.get("relationships", {})

    for key in ["id", "type"]:
        if not record.get(key):
            raise MissingKeyError(key)
        if attributes.get(key) or relationships.get(key):
            raise ForbiddenKeyError(key)

    obj = {"id": record["id"], "type": record["type"]}

    for key, val in attributes.items():
        obj[key] = val

    for key, val in relationships.items():
        val = val["data"]
        if included_record := next(
            (
                included_record
                for included_record in included
                if included_record["id"] == val["id"] and included_record["type"] == val["type"]
            ),
            None,
        ):
            val = deserialize_record(included_record, included)

        obj[key] = val

    return obj


@t.overload
def deserialize(data: Data[Record]) -> dict: ...
def deserialize(data: Data[list[Record]]) -> list[dict]:
    """Deserialize JSON:API Response into human readable value."""
    if not data.get("data"):
        raise MissingKeyError("data")

    included = data.get("included", [])

    if isinstance(data.get("data"), list):
        return [deserialize_record(record, included) for record in data["data"]]

    return deserialize_record(data["data"], included)
