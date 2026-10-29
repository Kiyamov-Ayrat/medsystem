from dataclasses import dataclass, field


@dataclass
class AppError(Exception):
    """Базовый класс для всех ошибок проекта"""

    message: str
    status_code: int = field(default=400, init=False)


@dataclass
class NotFoundError(AppError):
    """Ресурс не найден"""

    status_code: int = field(default=404, init=False)


@dataclass
class ConflictError(AppError):
    """Сырье с таким именем уже существует"""

    status_code: int = field(default=409, init=False)
