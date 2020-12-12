class CoreError(RuntimeError):
    pass


class CoreWarning(Warning):
    pass


class DataError(CoreError):
    pass


class GraphError(CoreWarning):
    pass
