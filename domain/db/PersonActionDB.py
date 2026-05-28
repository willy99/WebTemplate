from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import date
from typing import Optional, Any, Union
from dics.deserter_xls_dic import *

class PersonActionDB(BaseModel):
    # Дозволяє використовувати як назви змінних, так і аліаси (назви колонок Excel)
    model_config = ConfigDict(populate_by_name=True)

    deleted: int = Field(0, description="0 - активний, 1 - видалений")

    # Числові та ідентифікатори
    id: int = Field(None, alias=COLUMN_INCREMENTAL)
    person_id: int = Field(..., description="Посилання на ID з таблиці persons")
    mil_unit: Optional[str] = Field("", alias=COLUMN_MIL_UNIT)

    # Дати (тепер використовуємо Union, щоб бути гнучкими)
    insert_date: Optional[Union[date, str]] = Field(None, alias=COLUMN_INSERT_DATE)
    desertion_date: Optional[Union[date, str]] = Field(None, alias=COLUMN_DESERTION_DATE)
    raport_date: Optional[Union[date, str]] = Field(None, alias=COLUMN_REPORT_DATE)
    return_date: Optional[Union[date, str]] = Field(None, alias=COLUMN_RETURN_DATE)
    return_reserve_date: Optional[Union[date, str]] = Field(None, alias=COLUMN_RETURN_TO_RESERVE_DATE)

    o_ass_date: Optional[Union[date, str]] = Field("", alias=COLUMN_ORDER_ASSIGNMENT_DATE)
    o_res_date: Optional[Union[date, str]] = Field("", alias=COLUMN_ORDER_RESULT_DATE)
    kpp_date: Optional[Union[date, str]] = Field("", alias=COLUMN_KPP_DATE)
    dbr_date: Optional[Union[date, str]] = Field("", alias=COLUMN_DBR_DATE)
    erdr_date: Optional[Union[date, str]] = Field("", alias=COLUMN_ERDR_DATE)

    # Текстові поля (Short Input)
    desertion_place: Optional[str] = Field("", alias=COLUMN_DESERTION_PLACE)
    desertion_type: Optional[Union[str, int]] = Field("", alias=COLUMN_DESERTION_TYPE)
    desertion_region: Optional[str] = Field("", alias=COLUMN_DESERTION_REGION)
    executor: Optional[str] = Field("", alias=COLUMN_EXECUTOR)
    desertion_term: Optional[str] = Field("", alias=COLUMN_DESERTION_TERM)

    review_status: Optional[str] = Field("", alias=COLUMN_REVIEW_STATUS)
    o_ass_num: Optional[Union[str, int]] = Field("", alias=COLUMN_ORDER_ASSIGNMENT_NUMBER)
    o_res_num: Optional[Union[str, int]] = Field("", alias=COLUMN_ORDER_RESULT_NUMBER)
    cc_article: Optional[Union[str, int]] = Field("", alias=COLUMN_CC_ARTICLE)
    kpp_num: Optional[Union[str, int]] = Field("", alias=COLUMN_KPP_NUMBER)
    dbr_num: Optional[Union[str, int]] = Field("", alias=COLUMN_DBR_NUMBER)
    erdr_notation: Optional[Union[str, int]] = Field("", alias=COLUMN_ERDR_NOTATION)
    notation: Optional[Union[str, int]] = Field("", alias=COLUMN_NOTATION)

    title: Optional[str] = Field("", alias=COLUMN_TITLE)
    title2: Optional[str] = Field("", alias=COLUMN_TITLE_2)
    subunit: Optional[str] = Field("", alias=COLUMN_SUBUNIT)
    subunit2: Optional[str] = Field("", alias=COLUMN_SUBUNIT2)

    # Великі текстові поля (Textarea)
    desertion_conditions: Optional[str] = Field("", alias=COLUMN_DESERT_CONDITIONS)


    @field_validator('o_res_num', 'o_ass_num', "kpp_num", "dbr_num", "cc_article", "erdr_notation", mode='before')
    @classmethod
    def ensure_string_or_empty(cls, v: Any):
        if v is None:
            return ""
        if isinstance(v, (int, float)):
            return str(int(v)) if v == int(v) else str(v)
        return str(v).strip()
