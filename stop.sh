#!/bin/bash

# 定义PID文件
PID_FILE="auto_blive_gift.pid"

# 检查PID文件是否存在
if [ ! -f $PID_FILE ]; then
    echo "PID文件不存在，无法关闭程序"
    exit 1
fi

# 读取PID，并尝试关闭程序
PID=$(cat $PID_FILE)
kill -9 $PID

if [ $? -eq 0 ]; then
    echo "程序已关闭"
    rm $PID_FILE
else
    echo "无法关闭程序"
fi
