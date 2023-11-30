#!/bin/sh
set -e

OUTDIR="/backend/out"

cd /backend

cp -r /wakeonlan /backend/out
cp -r /protobuf /backend/out