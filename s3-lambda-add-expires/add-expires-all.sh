#!/bin/sh

set -eux

BUCKET=$1
DATE=$(TZ=JST+15 date --iso-8601=seconds -d '365 days')
echo "$DATE"

PYTHONIOENCODING=UTF-8 aws s3 ls "s3://$BUCKET" --recursive |\
  grep -E ".*\.(jpg|png|gif|svg)$" |\
  awk -v BUCKET="${BUCKET}" -v DATE="${DATE}" '{system("aws s3api copy-object --bucket " BUCKET " --copy-source " BUCKET "/" $4 " --key " $4 " --metadata-directive REPLACE --expires " DATE )}'
