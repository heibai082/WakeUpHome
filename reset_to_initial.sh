#!/bin/bash
ANCHOR_FILE="/opt/Initial_Anchor_v0.0.705_ORIGINAL.tar.gz"
if [ ! -f "$ANCHOR_FILE" ]; then echo "错误：未找到 v0.0.705 锚点文件！"; exit 1; fi
echo "系统回滚至 v0.0.705 智慧日志版..."
systemctl stop wakeup.service
tar -xzf $ANCHOR_FILE -C /
systemctl restart wakeup.service
echo "回滚成功！"
