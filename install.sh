#!/bin/bash
# 醒醒宅家 (WakeUpHome) v0.0.735 一键部署脚本

echo "🚀 开始为 Debian 13 环境安装杰作版..."

# 1. 安装核心系统依赖
apt update && apt install -y python3 python3-venv sqlite3 git curl

# 2. 准备运行目录
mkdir -p /opt/WakeUpHome
cd /opt/WakeUpHome

# 3. 部署 Python 虚拟环境与必要包
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install fastapi uvicorn httpx python-multipart

# 4. 物理固化 Systemd 后台服务
cat << 'SYS_EOF' > /etc/systemd/system/wakeup.service
[Unit]
Description=WakeUpHome Masterpiece Service
After=network.target

[Service]
User=root
WorkingDirectory=/opt/WakeUpHome
ExecStart=/opt/WakeUpHome/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
SYS_EOF

# 5. 激活并通电
systemctl daemon-reload
systemctl enable wakeup.service
systemctl start wakeup.service

echo "✅ 安装成功！请通过 http://服务器IP:8000 访问您的权柄中心。"
