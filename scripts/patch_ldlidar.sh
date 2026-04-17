#!/usr/bin/env bash
set -e

WORKSPACE="${HOME}/ldlidar_ros2_ws"
FILE="${WORKSPACE}/src/ldlidar_stl_ros2/ldlidar_driver/include/logger/log_module.h"

if [ ! -f "$FILE" ]; then
  echo "File not found: $FILE"
  exit 1
fi

sed -i 's@^[[:space:]]*//[[:space:]]*#include <pthread.h>@#include <pthread.h>@' "$FILE"

echo "Patched: $FILE"
grep -n "pthread.h" "$FILE"
