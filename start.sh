#!/bin/bash
#如果程序已经启动，那么先关闭
if [ -f "auto_blive_gift.pid" ]; then
    echo "程序已经启动，PID: $(cat auto_blive_gift.pid)，正在关闭..."
    kill -9 $(cat auto_blive_gift.pid)
    rm -f auto_blive_gift.pid
    echo "程序已关闭"
fi

LOG_FILE="auto_blive_gift.log"
PID_FILE="auto_blive_gift.pid"

# 进入目录


# 启动程序，并将输出重定向到日志文件
nohup python src/main.py --job-name auto_blive_gift > $LOG_FILE 2>&1 &

# 保存PID到文件
echo $! > $PID_FILE

echo "程序已启动，PID: $(cat $PID_FILE)"
