from decimal import Decimal
import typing
from typing import (Any, Dict, Iterable, Iterator, List, Mapping, NamedTuple,
                    Tuple, TypedDict)

from .abstracts import MySQLConnectionAbstract as MySQLConnectionAbstract

# from .abstracts import MySQLCursorAbstract as MySQLCursorAbstract

class GetRowStatus(TypedDict):
    warning_count: int
    status_flag: int

class StmtInfo(TypedDict):
    statement_id: int
    num_columns: int
    num_params: int
    warning_count: int
    columns: List[Tuple[Any, ...]]
    parameters: List[Any]

class MySQLConnection(MySQLConnectionAbstract):
    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None: ...
    def shutdown(self) -> None: ...
    def close(self) -> None: ...

    disconnect: Any = ...

    @property
    def in_transaction(self) -> bool: ...
    def get_row(
        self,
        binary: bool = ...,
        columns: Any | None = ...,
    ) -> Tuple[Tuple[Any, ...], None] | Tuple[None, GetRowStatus]: ...
    def get_rows(
        self,
        count: Any | None = ...,
        binary: bool | None = ...,
        columns: Any | None = ...,
    ) -> Tuple[List[Tuple[Any, ...]], GetRowStatus]: ...
    def consume_results(self) -> None: ...
    def cmd_init_db(
        self,
        database: Any,
    ) -> Mapping[str, Any]: ...
    def cmd_query(
        self,
        query: Any,
        raw: bool = ...,
        buffered: bool = ...,
        raw_as_string: bool = ...,
    ) -> Any: ...
    def cmd_query_iter(
        self,
        statements: Any,
    ) -> None: ...
    def cmd_refresh(
        self,
        options: Any,
    ) -> Mapping[str, int]: ...
    def cmd_quit(self) -> bytearray: ...
    def cmd_shutdown(
        self,
        shutdown_type: Any | None = ...,
    ) -> Mapping[str, int]: ...
    def cmd_statistics(self) -> Mapping[str, int | Decimal]: ...
    def cmd_process_kill(
        self,
        mysql_pid: Any,
    ) -> Mapping[str, int]: ...
    def cmd_debug(self) -> Mapping[str, int]: ...
    def cmd_ping(self) -> Mapping[str, int]: ...
    def cmd_change_user(
        self,
        username: str = ...,
        password: str = ...,
        database: str = ...,
        charset: int = ...,
    ) -> Mapping[str, int]: ...
    @property
    def database(self) -> MySQLConnection: ...
    @database.setter
    def database(self, value: Any) -> MySQLConnection: ...
    def is_connected(self) -> bool: ...
    def reset_session(
        self,
        user_variables: Any | None = ...,
        session_variables: Any | None = ...,
    ) -> None: ...
    def reconnect(self, attempts: int = ..., delay: int = ...) -> None: ...
    def ping(
        self, reconnect: bool = ..., attempts: int = ..., delay: int = ...
    ) -> None: ...
    @property
    def connection_id(self) -> int: ...
    def cursor(
        self,
        buffered: Any | None = ...,
        raw: Any | None = ...,
        prepared: Any | None = ...,
        cursor_class: Any | None = ...,
        dictionary: Any | None = ...,
        named_tuple: Any | None = ...,
    ) -> MySQLCursor: ...
    # ) -> MySQLCursorAbstract: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def info_query(self, query: Any) -> Tuple[Any, ...]: ...
    def cmd_stmt_prepare(self, statement: Any) -> StmtInfo: ...
    def cmd_stmt_execute(
        self,
        statement_id: Any,
        data: Any = ...,
        parameters: Any = ...,
        flags: int = ...,
    ) -> Any: ...
    def cmd_stmt_close(self, statement_id: Any) -> None: ...
    def cmd_stmt_send_long_data(
        self, statement_id: Any, param_id: Any, data: Any
    ) -> Any: ...
    def cmd_stmt_reset(self, statement_id: Any) -> None: ...
    def cmd_reset_connection(self) -> None: ...
    def handle_unread_result(self) -> None: ...

class ColDescription(NamedTuple):
    column_name: str
    type: str
    _: None
    _: None
    _: None
    _: None
    null_ok: bool
    column_flags: Tuple[str]


ExecuteParams: typing.TypeAlias = Tuple[Any, ...] | List[Any] | Dict[str, Any]


class MySQLCursor:
    def __init__(
        self,
        connection: MySQLConnection | None = ...,
    ) -> None: ...
    def callproc(
        self,
        procname: str,
        args: Tuple[Any, ...] = ...,
    ) -> None:
        """Calls a stored procedue with the given arguments

        The arguments will be set during this session, meaning
        they will be called like  _<procname>__arg<nr> where
        <nr> is an enumeration (+1) of the arguments.

        Coding Example:
          1) Definining the Stored Routine in MySQL:
          CREATE PROCEDURE multiply(IN pFac1 INT, IN pFac2 INT, OUT pProd INT)
          BEGIN
            SET pProd := pFac1 * pFac2;
          END

          2) Executing in Python:
          args = (5,5,0) # 0 is to hold pprod
          cursor.callproc('multiply', args)
          print(cursor.fetchone())

        Does not return a value, but a result set will be
        available when the CALL-statement execute successfully.
        Raises exceptions when something is wrong.
        """
        ...
    def close(self) -> None:
        """Close the cursor."""
        ...
    def execute(
        self,
        operation: str,
        params: ExecuteParams | None = ...,
        multi: bool = ...,
    ) -> None:
        """Executes the given operation

        Executes the given operation substituting any markers with
        the given parameters.

        For example, getting all rows where id is 5:
          cursor.execute("SELECT * FROM t1 WHERE id = %s", (5,))

        The multi argument should be set to True when executing multiple
        statements in one operation. If not set and multiple results are
        found, an InterfaceError will be raised.

        If warnings where generated, and connection.get_warnings is True, then
        self._warnings will be a list containing these warnings.

        Returns an iterator when multi is True, otherwise None.
        """
        ...
    def executemany(
        self,
        operation: str,
        params: Tuple[ExecuteParams, ...] | List[ExecuteParams],
    ) -> None:
        """Execute the given operation multiple times

        The executemany() method will execute the operation iterating
        over the list of parameters in seq_params.

        Example: Inserting 3 new employees and their phone number

        data = [
            ('Jane','555-001'),
            ('Joe', '555-001'),
            ('John', '555-003')
            ]
        stmt = "INSERT INTO employees (name, phone) VALUES ('%s','%s')"
        cursor.executemany(stmt, data)

        INSERT statements are optimized by batching the data, that is
        using the MySQL multiple rows syntax.

        Results are discarded. If they are needed, consider looping over
        data using the execute() method.
        """
        ...
    def fetchall(self) -> List[Tuple[Any, ...]]:
        """Returns all rows of a query result set

        Returns a list of tuples.
        """
        ...
    def fetchmany(self, size: int = ...) -> List[Tuple[Any, ...]]:
        """Returns the next set of rows of a query result, returning a
        list of tuples. When no more rows are available, it returns an
        empty list.

        The number of rows returned can be specified using the size argument,
        which defaults to one
        """
    def fetchone(self) -> Tuple[Any, ...]:
        """Returns next row of a query result set

        Returns a tuple or None.
        """
        ...
    def fetchwarnings(self) -> List[Tuple[str, int, str]] | None:
        """
        Fetch warnings doing a SHOW WARNINGS. Can be called after getting
        the result.

        Returns a result set or None when there were no warnings.
        """
        ...
    def stored_results(self) -> Iterator[Tuple[Any, ...]]:
        """Returns an iterator for stored results

        This method returns an iterator over results which are stored when
        callproc() is called. The iterator will provide MySQLCursorBuffered
        instances.

        Returns a iterator.
        """
        ...
    @property
    def column_names(self) -> Tuple[str, ...]:
        """Returns column names

        This property returns the columns names as a tuple.

        Returns a tuple.
        """
        ...
    @property
    def description(self) -> List[ColDescription]:
        """Returns description of columns in a result

        This property returns a list of tuples describing the columns in
        in a result set. A tuple is described as follows::

                (column_name,
                 type,
                 None,
                 None,
                 None,
                 None,
                 null_ok,
                 column_flags)  # Addition to PEP-249 specs

        Returns a list of tuples.
        """
        ...
    @property
    def lastrowid(self) -> int:
        """Returns the value generated for an AUTO_INCREMENT column

        Returns the value generated for an AUTO_INCREMENT column by
        the previous INSERT or UPDATE statement or None when there is
        no such value available.

        Returns a long value or None.
        """
        ...
    @property
    def rowcount(self) -> int:
        """Returns the number of rows produced or affected

        This property returns the number of rows produced by queries
        such as a SELECT, or affected rows when executing DML statements
        like INSERT or UPDATE.

        Note that for non-buffered cursors it is impossible to know the
        number of rows produced before having fetched them all. For those,
        the number of rows will be -1 right after execution, and
        incremented when fetching rows.

        Returns an integer.
        """
        ...
    @property
    def statement(self) -> str:
        """Returns the executed statement

        This property returns the executed statement. When multiple
        statements were executed, the current statement in the iterator
        will be returned.
        """
        ...
    @property
    def with_rows(self) -> bool:
        """Returns whether the cursor could have rows returned

        This property returns True when column descriptions are available
        and possibly also rows, which will need to be fetched.

        Returns True or False.
        """
        ...
