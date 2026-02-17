"""
Вспомогательные функции.
"""


def escape_md(text: str) -> str:
    """Экранирование спецсимволов для Markdown V1.
    В Markdown V1 нужно экранировать: _ * [ ] ( ) ~ ` > # + - = | { } . !
    Но для простоты экранируем только основные проблемные."""
    if not text:
        return ""
    for char in ['_', '*', '[', ']', '(', ')', '~', '`']:
        text = text.replace(char, f'\\{char}')
    return text


def safe_name(name) -> str:
    """Безопасное имя для вставки в Markdown."""
    if not name:
        return "—"
    return str(name)