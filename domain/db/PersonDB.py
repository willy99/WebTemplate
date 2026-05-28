from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional, Any, Union
from dics.deserter_xls_dic import *

class PersonDB(BaseModel):
    # Дозволяє використовувати як назви змінних, так і аліаси (назви колонок Excel)
    model_config = ConfigDict(populate_by_name=True)

    deleted: int = Field(0, description="0 - активний, 1 - видалений")

    # Числові та ідентифікатори
    id: int = Field(None, alias=COLUMN_INCREMENTAL)

    # Дати (тепер використовуємо Union, щоб бути гнучкими)
    birthday: Optional[Union[date, str]] = Field(None, alias=COLUMN_BIRTHDAY)
    enlistment_date: Optional[Union[date, str]] = Field(None, alias=COLUMN_ENLISTMENT_DATE)

    # Текстові поля (Short Input)
    name: str = Field("", alias=COLUMN_NAME)
    rnokpp: Optional[Any] = Field(None, alias=COLUMN_ID_NUMBER)
    address: Optional[str] = Field("", alias=COLUMN_ADDRESS)
    phone: Optional[str] = Field("", alias=COLUMN_PHONE)

    service_type: Optional[str] = Field("", alias=COLUMN_SERVICE_TYPE)
    tzk: Optional[str] = Field("", alias=COLUMN_TZK)
    tzk_region: Optional[str] = Field("", alias=COLUMN_TZK_REGION)
    suspended: Optional[Union[int, str]] = Field("", alias=COLUMN_SUSPENDED)

    # Великі текстові поля (Textarea)
    bio: Optional[str] = Field("", alias=COLUMN_BIO)

    # calculated
#    service_days: Optional[Union[str, int]] = Field(None, alias=COLUMN_SERVICE_DAYS)
#    experience: Optional[Union[str, int]] = Field("", alias=COLUMN_EXPERIENCE)

    # virtual fields
    matched_voc_info: Optional[str] = ""
