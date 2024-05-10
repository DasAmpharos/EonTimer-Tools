from PySide6.QtCore import QSettings


def get_settings() -> QSettings:
    return QSettings(
        QSettings.defaultFormat(),
        QSettings.Scope.UserScope,
        'io.github.dasampharos',
        'EonTimer'
    )
