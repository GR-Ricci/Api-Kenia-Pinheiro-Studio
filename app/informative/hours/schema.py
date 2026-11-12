from pydantic import BaseModel


class HorarioSlot(BaseModel):
    abertura: str   # "09:00"
    fechamento: str # "18:00"


class FuncionamentoDiaUpdate(BaseModel):
    horarios: list[HorarioSlot]


class FuncionamentoDiaResponse(BaseModel):
    dia: int
    horarios: list[HorarioSlot]