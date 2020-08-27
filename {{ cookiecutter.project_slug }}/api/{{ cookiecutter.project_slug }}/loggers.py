import logging

import pygments
import sqlparse

from pygments.formatters.terminal256 import TerminalTrueColorFormatter
from pygments.lexers.sql import SqlLexer


class SQLFormatter(logging.Formatter):
    def format(self, record):
        sql = sqlparse.format(record.sql.strip(), reindent=True)
        record.statement = pygments.highlight(sql, SqlLexer(), TerminalTrueColorFormatter(style="monokai"))
        return super().format(record)
