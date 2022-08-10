from __future__ import annotations

import typing
from decimal import Decimal

from .abstracts import MySQLConnectionAbstract as MySQLConnectionAbstract

# from .abstracts import MySQLCursorAbstract as MySQLCursorAbstract

class GetRowStatus(typing.TypedDict):
    warning_count: int
    status_flag: int

class StmtInfo(typing.TypedDict):
    statement_id: int
    num_columns: int
    num_params: int
    warning_count: int
    columns: list[tuple[typing.Any, ...]]
    parameters: list[typing.Any]

Row: typing.TypeAlias = tuple[typing.Any, ...]

class MySQLConnection(MySQLConnectionAbstract):
    def __init__(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None: ...
    def shutdown(self) -> None: ...
    def close(self) -> None: ...

    disconnect: typing.Any = ...

    @property
    def in_transaction(self) -> bool: ...
    def get_row(
        self,
        binary: bool = ...,
        columns: typing.Any | None = ...,
    ) -> tuple[Row, None] | tuple[None, GetRowStatus]: ...
    def get_rows(
        self,
        count: typing.Any | None = ...,
        binary: bool | None = ...,
        columns: typing.Any | None = ...,
    ) -> tuple[list[Row], GetRowStatus]: ...
    def consume_results(self) -> None: ...
    def cmd_init_db(
        self,
        database: typing.Any,
    ) -> typing.Mapping[str, typing.Any]: ...
    def cmd_query(
        self,
        query: typing.Any,
        raw: bool = ...,
        buffered: bool = ...,
        raw_as_string: bool = ...,
    ) -> typing.Any: ...
    def cmd_query_iter(
        self,
        statements: typing.Any,
    ) -> None: ...
    def cmd_refresh(
        self,
        options: typing.Any,
    ) -> typing.Mapping[str, int]: ...
    def cmd_quit(self) -> bytearray: ...
    def cmd_shutdown(
        self,
        shutdown_type: typing.Any | None = ...,
    ) -> typing.Mapping[str, int]: ...
    def cmd_statistics(self) -> typing.Mapping[str, int | Decimal]: ...
    def cmd_process_kill(
        self,
        mysql_pid: typing.Any,
    ) -> typing.Mapping[str, int]: ...
    def cmd_debug(self) -> typing.Mapping[str, int]: ...
    def cmd_ping(self) -> typing.Mapping[str, int]: ...
    def cmd_change_user(
        self,
        username: str = ...,
        password: str = ...,
        database: str = ...,
        charset: int = ...,
    ) -> typing.Mapping[str, int]: ...
    @property
    def database(self) -> MySQLConnection: ...
    @database.setter
    def database(self, value: typing.Any) -> MySQLConnection: ...
    def is_connected(self) -> bool: ...
    def reset_session(
        self,
        user_variables: typing.Any | None = ...,
        session_variables: typing.Any | None = ...,
    ) -> None: ...
    def reconnect(self, attempts: int = ..., delay: int = ...) -> None: ...
    def ping(
        self, reconnect: bool = ..., attempts: int = ..., delay: int = ...
    ) -> None: ...
    @property
    def connection_id(self) -> int: ...
    def cursor(
        self,
        buffered: typing.Any | None = ...,
        raw: typing.Any | None = ...,
        prepared: typing.Any | None = ...,
        cursor_class: typing.Any | None = ...,
        dictionary: typing.Any | None = ...,
        named_tuple: typing.Any | None = ...,
    ) -> MySQLCursor: ...
    # ) -> MySQLCursorAbstract: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def info_query(self, query: typing.Any) -> tuple[typing.Any, ...]: ...
    def cmd_stmt_prepare(self, statement: typing.Any) -> StmtInfo: ...
    def cmd_stmt_execute(
        self,
        statement_id: typing.Any,
        data: typing.Any = ...,
        parameters: typing.Any = ...,
        flags: int = ...,
    ) -> typing.Any: ...
    def cmd_stmt_close(self, statement_id: typing.Any) -> None: ...
    def cmd_stmt_send_long_data(
        self, statement_id: typing.Any, param_id: typing.Any, data: typing.Any
    ) -> typing.Any: ...
    def cmd_stmt_reset(self, statement_id: typing.Any) -> None: ...
    def cmd_reset_connection(self) -> None: ...
    def handle_unread_result(self) -> None: ...

ExecuteParams: typing.TypeAlias = (
    tuple[typing.Any, ...] | list[typing.Any] | dict[str, typing.Any]
)

class ColDescription(typing.NamedTuple):
    column_name: str
    type: str
    _: None
    _: None
    _: None
    _: None
    null_ok: bool
    column_flags: tuple[str]

class MySQLCursor:
    def __init__(
        self,
        connection: MySQLConnection | None = ...,
    ) -> None: ...
    def callproc(
        self,
        procname: str,
        args: tuple[typing.Any, ...] = ...,
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
        params: typing.Iterable[ExecuteParams],
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
    def fetchall(self) -> list[tuple[typing.Any, ...]]:
        """Returns all rows of a query result set

        Returns a list of tuples.
        """
        ...
    def fetchmany(self, size: int = ...) -> list[tuple[typing.Any, ...]]:
        """Returns the next set of rows of a query result, returning a
        list of tuples. When no more rows are available, it returns an
        empty list.

        The number of rows returned can be specified using the size argument,
        which defaults to one
        """
    def fetchone(self) -> tuple[typing.Any, ...]:
        """Returns next row of a query result set

        Returns a tuple or None.
        """
        ...
    def _fetch_warnings(self) -> list[str] | None:
        """
        Fetch warnings doing a SHOW WARNINGS. Can be called after getting
        the result.

        Returns a result set or None when there were no warnings.
        """
        ...
    def stored_results(self) -> typing.Iterator[tuple[typing.Any, ...]]:
        """Returns an iterator for stored results

        This method returns an iterator over results which are stored when
        callproc() is called. The iterator will provide MySQLCursorBuffered
        instances.

        Returns a iterator.
        """
        ...
    @property
    def column_names(self) -> tuple[str, ...]:
        """Returns column names

        This property returns the columns names as a tuple.

        Returns a tuple.
        """
        ...
    @property
    def description(self) -> list[ColDescription]:
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
