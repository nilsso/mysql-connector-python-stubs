import typing

from .connection import MySQLConnection

def connect(*args: typing.Any, **kwargs: typing.Any) -> MySQLConnection:
    """Create or get a MySQL connection object

    In its simpliest form, Connect() will open a connection to a
    MySQL server and return a MySQLConnection object.

    When any connection pooling arguments are given, for example pool_name
    or pool_size, a pool is created or a previously one is used to return
    a PooledMySQLConnection.

    Returns MySQLConnection or PooledMySQLConnection.
    """
    ...


class Error(Exception):
    """Exception that is base class for all other error exceptions"""
    ...


class Warning(Exception):
    """Exception for important warnings"""


class InterfaceError(Error):
    """Exception for errors related to the interface"""


class DatabaseError(Error):
    """Exception for errors related to the database"""


class InternalError(DatabaseError):
    """Exception for errors internal database errors"""


class OperationalError(DatabaseError):
    """Exception for errors related to the database's operation"""


class ProgrammingError(DatabaseError):
    """Exception for errors programming errors"""


class IntegrityError(DatabaseError):
    """Exception for errors regarding relational integrity"""


class DataError(DatabaseError):
    """Exception for errors reporting problems with processed data"""


class NotSupportedError(DatabaseError):
    """Exception for errors when an unsupported database feature was used"""


class PoolError(Error):
    """Exception for errors relating to connection pooling"""
