#!/bin/bash
ANCHOR="/opt/Initial_Anchor_v0.0.707_ORIGINAL.tar.gz"
systemctl stop wakeup.service
tar -xzf $ANCHOR -C /
chmod -R 777 /opt/WakeUpHome
systemctl restart wakeup.service
echo "系统已强行回归至 v0.0.707 原始锚点版！"
