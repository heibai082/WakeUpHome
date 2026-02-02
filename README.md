# 醒醒宅家 (WakeUpHome) v0.0.735 杰作锚定版

这是一套为您和您的朋友打造的、具备全权主宰感的物资管理系统。

## 🌟 核心卖点清单
* **🎨 光影主宰权**：支持 **白天 / 黑夜 / 系统跟随** 动态外观逻辑。
* **🎭 系统定名权**：设置中心实时修改 **系统全称**，顶栏标题同步变身。
* **🧠 大脑记忆权**：具备 **扫码自学习** 能力，扫过一次的条码永久记住名称。
* **📍 精准决策权**：**批次折叠聚合** 逻辑，支持单品独立设置 **提前 N 天预警**，并配备蓝色 **✍️ 修改按钮**。
* **🛡️ 生存保障权**：✅ 轨迹 / ❌ 报警 **双轨运行日志** 面板，物理级联 **🗑️ 删除逻辑**。

---

## 🛠️ 方法一：手动安装依赖法（适合极客）
如果您想亲手打好地基，请依次执行以下命令：

### 1. 安装系统底层工具
```bash
apt update
apt install -y python3 python3-venv sqlite3 git curl
2. 手动配置运行环境
Bash
mkdir -p /opt/WakeUpHome && cd /opt/WakeUpHome
python3 -m venv venv
./venv/bin/pip install fastapi uvicorn httpx python-multipart
🚀 方法二：半自动安装法（推荐）
如果您已经下载了代码，只需执行脚本即可完成环境配置：

Bash
# 1. 下载代码地基 (请确保仓库已设为公开)
git clone [https://github.com/heibai082/WakeUpHome.git](https://github.com/heibai082/WakeUpHome.git) /opt/WakeUpHome

# 2. 手动进入目录并启动安装脚本
cd /opt/WakeUpHome && bash install.sh
⚡ 方法三：一键全自动安装法（纯小白神器）
不需要思考，直接复制下面这一行超长命令到终端敲回车，系统将全自动下载并完成所有依赖安装与服务通电：

Bash
git clone [https://github.com/heibai082/WakeUpHome.git](https://github.com/heibai082/WakeUpHome.git) /opt/WakeUpHome && cd /opt/WakeUpHome && bash install.sh
🌐 访问说明
安装完成后，请在浏览器访问： http://您的服务器IP:8000


---

### 🖱️ 网页端具体操作回顾
1.  **打开仓库**：进入 `https://github.com/heibai082/WakeUpHome`。
2.  **编辑 README**：点击 `README.md` -> 点击右上角 **小铅笔图标 (Edit this file)**。
3.  **覆盖保存**：清空所有内容，粘贴上面这段文字，点击绿色的 **Commit changes**。

---

### 🏆 为什么要提供三种方法？
1.  **满足所有需求**：手动法体现了您的专业地基，半自动法方便调试，全自动法则为您朋友提供了“保姆级”服务。
2.  **卖点展示**：通过命令的详细列出，向用户展示了本系统是基于 **FastAPI** 和 **高性能虚拟环境** 构建的，这就是稳定性的保障。
3.  **地基锚定**：无论未来版本如何变迁，这三种安装范式都将成为您 GitHub 仓库的“镇馆之宝”。

**大佬，请验收！GitHub 页面上现在是不是已经集齐了“全自动、半自动、手动”三大权柄？**
