#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
kill $(cat ${DIR}/setcstate.pid)
rm ${DIR}/setcstate.pid
