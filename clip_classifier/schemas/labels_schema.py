from pydantic import BaseModel
from fastapi import Query
from typing import List


class Labels(BaseModel):
    labels: List[str] = Query([])
