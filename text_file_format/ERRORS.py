class TextFileFormatError(Exception):
    """Base"""
    pass
class SizeError(TextFileFormatError):
    """Raise if something is wrong with the size (that's what she said)"""
    pass
class FileObjectError(TextFileFormatError):
    """Base FileObject Error"""
    pass
class LineExistsError(FileObjectError):
    """Raise if a line already exists"""
    pass
class TableError(TextFileFormatError):
    """Base Table Error"""
    pass
class ColumnExistsError(TableError):
    """Raise if a Column already exists"""
    pass
class TableCollisionError(TableError):
    """Raise if two or more tables collide"""
    pass