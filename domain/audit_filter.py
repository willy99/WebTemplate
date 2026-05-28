from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class AuditSearchFilter:
    # Дата внесення (Рік)
    ins_year: Optional[Union[str, list]] = None

    check_rnokpp_dob: bool = False       # 1) рнокпп != дата народження
    check_title: bool = False            # 2) звання (порожнє або невідоме)
    check_mil_unit: bool = False         # 3) перевірка відповідності, де знаходиться чувак
    check_service_type: bool = False     # 4) вид служби
    check_critical_empty: bool = False   # 5) критичні помилки (ПІБ, № порожні)
    check_date_logic: bool = False       # 6) нелогічність у датах (сзч > повернення)
    check_future_dates: bool = False     # 7) майбутні дати