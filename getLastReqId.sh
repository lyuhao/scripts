#!/bin/bash

BINFILE=$1
awk '{w=$1} END{print w}' ${BINFILE}
