#!/bin/bash
NAME="auto_blive_gift"
LOG_FILE=$NAME".log"
PID_FILE=$NAME".pid"
#如果程序已经启动，那么先关闭
if [ -f $PID_FILE ]; then
    echo "程序已经启动，PID: $(cat $PID_FILE)，正在关闭..."
    kill -9 $(cat $PID_FILE)
    rm -f $PID_FILE
    echo "程序已关闭"
fi

# 进入目录

# 启动程序，并将输出重定向到日志文件
nohup python src/main.py --job-name auto_blive_gift > $LOG_FILE 2>&1 &

# 保存PID到文件
echo $! > $PID_FILE

echo "程序已启动，PID: $(cat $PID_FILE)"
