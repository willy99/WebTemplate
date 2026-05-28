from typing import List, Dict, Any
from pydantic import BaseModel

from domain.db.PersonActionDB import PersonActionDB
from domain.db.PersonDB import PersonDB


class PersonFullInfo(BaseModel):
    person: PersonDB
    actions: List[PersonActionDB]