#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python << END
import sys
import time

import psycopg

suggest_unrecoverable_after = 30
start = time.time()

while True:
    try:
        con = psycopg.connect(conninfo="${{ '{' }}{{ cookiecutter.__env_prefix }}DATABASE_URL}")
    except psycopg.OperationalError as error:
        sys.stderr.write("Waiting for PostgreSQL to become available...\n")

        if time.time() - start > suggest_unrecoverable_after:
            sys.stderr.write("  This is taking longer than expected. The following exception may be indicative of an unrecoverable error: '{}'\n".format(error))
    else:
        con.close()
        break
    time.sleep(1)
END

>&2 echo 'PostgreSQL is available'

exec "$@"
