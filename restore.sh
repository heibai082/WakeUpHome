#!/bin/bash
# 自动寻找最新的备份文件
LATEST_BACKUP=$(ls -t /opt/WakeUpHome_Anchor_*.tar.gz | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "错误：未找到任何锚点备份文件！"
    exit 1
fi

echo "正在从锚点恢复: $LATEST_BACKUP"

# 停止当前服务
systemctl stop wakeup.service

# 解压并覆盖当前文件
tar -xzf $LATEST_BACKUP -C /

# 重启服务
systemctl restart wakeup.service

echo "-----------------------------------"
echo "恢复成功！系统已回到锚点状态。"
echo "-----------------------------------"
