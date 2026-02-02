#!/bin/bash
# 定义备份文件名
BACKUP_FILE="/opt/WakeUpHome_Anchor_$(date +%Y%m%d).tar.gz"

echo "正在创建锚点备份..."
# 停止服务确保数据库文件不在写入
systemctl stop wakeup.service

# 打包代码、数据库和日志
tar -czf $BACKUP_FILE /opt/WakeUpHome/main.py /opt/WakeUpHome/index.html /opt/WakeUpHome/db/data.db

# 重启服务
systemctl start wakeup.service

echo "-----------------------------------"
echo "备份完成！锚点文件存放在: $BACKUP_FILE"
echo "建议您把这个文件下载并存放到您的绿联 4800 NAS 上。"
echo "-----------------------------------"
