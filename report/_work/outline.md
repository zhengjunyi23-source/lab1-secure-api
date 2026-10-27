# Lab 1 报告 Outline

**写作类型**：学术实验报告（academics.md）；载体 Word。

## 封面（Title Page）
- Work 1: Secure REST API Development with CI/CD and Real CVE Vulnerability Analysis
- Variant number: CVE-2020-1938
- Surname and Name: Zheng Junyi
- HDU number: 23320127
- 落款：日期

## 1. Purpose
- 说明目标：安全 API 全生命周期（OWASP Top10 防护、CI/CD 自动安全扫描、真实 CVE 复现与修复）。

## 2. Choosing a Stack and Initializing the Project
- 技术栈：Python 3 + Flask + SQLAlchemy + PyJWT + bcrypt
- 包管理：pip + venv
- git init + 本地仓库；远程 GitHub 仓库链接（占位，待授权后填 URL）

## 3. Developing a Functional API
- 3 个端点：POST /auth/login、GET /api/data（需 JWT）、GET /api/me（需 JWT）
- 数据库：SQLite，种子用户 alice/bob/mallory
- 测试：pytest 7 项全部通过

## 4. Implementing Basic Security Measures
- SQLi：SQLAlchemy ORM 参数绑定（+ 测试证明 `' OR '1'='1'` 无效）
- XSS：递归 HTML 转义 xss_safe（+ 测试证明 `<script>` 被转义为 `&lt;script&gt;`）
- Broken Authentication：bcrypt 哈希、JWT 签发、@require_token 中间件校验、登录错误统一 401 防枚举

## 5. Setting Up a CI/CD Pipeline with Security Scanners
- .github/workflows/ci.yml：pytest + Bandit(SAST) + Safety(SCA)，上传报告 artifact
- 本地验证：bandit 0 问题、safety 0 漏洞
- GitHub Actions 运行结果与链接（占位，待授权后填 + 截图）

## 6. Selecting and Preparing a Vulnerable Environment
- Vulhub：git clone，进入 tomcat/CVE-2020-1938，docker compose up -d

## 7. Launching the Vulnerable Environment and Reproducing the Attack
- 启动 Tomcat 9.0.30，HTTP 8080 + AJP 8009
- PoC：python poc.py 127.0.0.1 -p 8009 -f WEB-INF/web.xml → 成功读取 web.xml（任意文件读取）

## 8. Analyzing the Root Cause of the Vulnerability
- CVE-2020-1938 定义（Ghostcat，Tomcat AJP 未认证任意文件读取）
- 根因：AJP Connector 默认开启、未绑定地址、无 secret/requiredSecret，Tomcat 信任 AJP 客户端属性 → 属于配置/输入处理缺陷
- 引用 server.xml 原文

## 9. Developing and Applying Protection Measures
- 修复：禁用 AJP 连接器（server.xml）+ docker-compose 不再暴露 8009 + Dockerfile 覆盖
- 修复文件：cve-2020-1938-fix/ 文件夹

## 10. Verifying the Fix
- AJP 8009 不再监听；PoC 重跑 → ConnectionRefusedError
- 回归：HTTP 8080 → 200（Tomcat 欢迎页正常）

## 11. What Students Submit / 提交物映射
- 公开仓库链接（占位）
- README.md 全文（见仓库）
- 最后一次 pipeline run 链接（占位）
- 修复文件包（已提供）
- 控制问题答案（1–8）

## 参考与致谢
- 引用：OWASP Top10、jwt.io、Vulhub、NVD/CVE 官方、Apache Tomcat 官方公告

## 附录
- 命令输出原文（复现/修复/API 调用）
- 截图占位说明（GitHub CI 部分）
