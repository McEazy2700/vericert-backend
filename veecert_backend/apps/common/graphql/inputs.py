from typing import Generic, Optional, TypeVar
import strawberry

Ordering = TypeVar("Ordering")
Filter = TypeVar("Filter")

Unordered = None
Unfiltered = None


@strawberry.input
class ListOptions(Generic[Filter, Ordering]):
    limit: Optional[int] = None
    offset: Optional[int] = None
    filter: Optional[Filter] = Unfiltered
    ordering: Optional[Ordering] = Unordered
