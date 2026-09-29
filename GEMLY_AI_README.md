# Gemly AI · Crystal Advisor 对话抽屉组件 · 部署说明文档

> 组件版本：v2.0（自研樱花粉白主题·后端代理架构）
> 适用项目：Haven Gems 晶石独立站
> 最后更新：2026-08-09
> 集成状态：✅ 已集成至全站 15 个业务页面

---

## 一、组件概览

| 项目 | 说明 |
|---|---|
| 组件名称 | Gemly AI · Crystal Advisor（樱花粉白自研对话抽屉） |
| 技术栈 | 原生 HTML + Tailwind CSS + 原生 JavaScript（无第三方 UI 库） |
| 触发按钮 id | `openGemlyAiBtn` |
| 弹窗形态 | 右侧固定抽屉（非模态居中弹窗） |
| PC 端尺寸 | 宽度 420px，高度 100vh，顶部贴合浏览器顶部 |
| 移动端尺寸 | 全屏宽度，从右侧滑入 |
| 主题配色 | 樱花粉白（主色 #FFD1DC，底色 #FFF8FA） |
| 对话能力 | 自研对话 UI + 后端代理调用 Coze 开放 API |
| 安全架构 | PAT 令牌仅存后端，前端零密钥暴露 |
| 演示模式 | 内置本地模拟回复开关（仅调试，禁止上线） |

---

## 二、⚠️ 安全警告（必读）

### 2.1 PAT 个人访问令牌安全红线

> **🚨 pat_ 开头的个人访问令牌（PAT）属于密钥，绝对不能部署到前端浏览器代码！**
> 前端代码任何人都能查看源码，一旦写入 PAT 令牌，等同于公开泄露，会被恶意调用消耗你的额度甚至造成数据泄露。

**正确做法**：
- ✅ PAT 令牌只能存放在**后端服务**的环境变量或密钥管理服务中
- ✅ 前端通过调用**自己的后端代理接口**间接获取 AI 回复
- ❌ 严禁将 PAT 写入 HTML / JS / 任何前端文件
- ❌ 严禁将 PAT 提交到 Git 仓库

### 2.2 架构示意

```
浏览器前端(本组件)  ──POST──>  你的后端代理接口  ──携带PAT──>  Coze开放API
  (无密钥)                      (存PAT令牌)                    (返回AI回复)
       ↑                            ↓
       └─────── JSON {reply} ───────┘
```

---

## 三、配置项说明

组件 JS 内置 3 个配置变量，位于 `<script>` 块顶部的「配置区」：

```javascript
/* ========= 配置区(上线前必读) ========= */
// ① 演示模式开关：true=本地模拟回复(仅调试用,禁止上线)；false=走后端代理调用真实AI
var GEMLY_DEMO_MODE = true;

// ② 后端代理接口地址(演示模式关闭后生效)
//    ⚠️ ①需要后端实现的代理接口地址位置
var GEMLY_PROXY_URL = '/api/gemly-chat';

// ③ Coze agent_id(智能体ID,可放前端；PAT个人访问令牌严禁写前端,只能放后端)
//    ⚠️ ②需要填写的Coze agent_id
var GEMLY_AGENT_ID = '';
/* ========= 配置区结束 ========= */
```

### 配置项详解

| 变量 | 位置 | 说明 | 安全等级 |
|---|---|---|---|
| `GEMLY_DEMO_MODE` | 前端 | 演示模式开关。`true`=模拟回复(调试)；`false`=真实API | 可放前端 |
| `GEMLY_PROXY_URL` | 前端 | ①后端代理接口地址，由你的后端实现 | 可放前端 |
| `GEMLY_AGENT_ID` | 前端 | ②Coze 智能体 ID，在 Coze 平台获取 | 可放前端（非密钥） |
| **PAT 令牌** | **后端** | pat_ 开头的个人访问令牌 | **🚨 严禁前端** |

### 在哪里替换 Coze API 密钥与 agent_id

| 配置 | 替换位置 | 操作 |
|---|---|---|
| **agent_id** | 前端组件 JS 配置区 `GEMLY_AGENT_ID` | 在 Coze 平台智能体详情页复制 ID，填入引号内 |
| **PAT 令牌** | 后端代理服务的环境变量 | 配置在后端（如 `COZE_PAT=pat_xxxxx`），前端永远不接触 |

---

## 四、触发按钮 id 要求

### 4.1 关键 id 约定

组件 JS 通过 `document.getElementById` 获取元素，**触发按钮必须设置 `id="openGemlyAiBtn"`**。

| 元素 | 必需 id | 作用 |
|---|---|---|
| 触发按钮 | `openGemlyAiBtn` | 点击打开抽屉（核心入口） |
| 抽屉容器 | `gemlyDrawer` | 抽屉主体 `<aside>` |
| 关闭按钮 | `gemlyDrawerClose` | 抽屉顶部 X 按钮 |
| 收起按钮 | `gemlyDrawerHide` | 抽屉顶部 › 按钮 |
| 对话滚动区 | `gemlyChatBody` | 渲染对话历史 |
| 输入框 | `gemlyInput` | 用户输入文本 |
| 发送按钮 | `gemlySendBtn` | 发送消息 |
| 遮罩层 | `gemlyDrawerBackdrop` | 移动端点击关闭 |

### 4.2 页面挂载方式

现有页面只需要保留触发按钮：

```html
<button id="openGemlyAiBtn" class="agent-fab" aria-label="Chat with Crystal Soul" title="与Crystal Soul（晶灵）对话">
    <i class="fa fa-comments text-xl"></i>
</button>
```

随后粘贴完整组件代码块（见第六节）。组件块位于按钮之后、`</body>` 之前。

---

## 五、演示模式开关用法

### 5.1 本地调试（模拟对话效果）

默认 `GEMLY_DEMO_MODE = true`，组件使用内置模拟回复，无需后端、无需密钥即可预览 UI 与交互：

```javascript
var GEMLY_DEMO_MODE = true;  // 本地调试用,模拟回复
```

模拟回复内容为晶石疗愈品牌相关文案，随机返回。**⚠️ 此模式仅本地调试，禁止上线**——用户收到的都是假回复，且未对接真实智能体。

### 5.2 上线模式（真实 AI 对话）

上线前改为 `false`，并配置后端代理接口与 agent_id：

```javascript
var GEMLY_DEMO_MODE = false;           // 关闭演示模式
var GEMLY_PROXY_URL = '/api/gemly-chat'; // 你的后端代理接口
var GEMLY_AGENT_ID = '你的智能体ID';     // Coze平台获取
```

同时后端需实现代理接口（见第七节）。

---

## 六、完整组件代码（可直接粘贴）

将以下整块代码粘贴到每个 HTML 页面的触发按钮之后、`</body>` 之前：

```html
<!-- ============ Gemly AI 对话抽屉组件（自研樱花粉白主题·不嵌入任何第三方页面） ============ -->
<aside id="gemlyDrawer" class="gemly-drawer" aria-hidden="true" role="dialog" aria-label="Gemly AI Crystal Advisor">
    <header class="gemly-header">
        <div class="gemly-header-info">
            <span class="gemly-header-icon"><i class="fa fa-gem"></i></span>
            <div class="min-w-0">
                <h3 class="gemly-header-title">Gemly AI · Crystal Advisor</h3>
                <p class="gemly-header-sub">Crystal Soul｜人宠晶石疗愈顾问</p>
            </div>
        </div>
        <div class="gemly-header-actions">
            <button id="gemlyDrawerHide" class="gemly-icon-btn" aria-label="收起" title="收起"><i class="fa fa-angle-right"></i></button>
            <button id="gemlyDrawerClose" class="gemly-icon-btn" aria-label="关闭" title="关闭"><i class="fa fa-times"></i></button>
        </div>
    </header>
    <div id="gemlyChatBody" class="gemly-chat-body"></div>
    <footer class="gemly-input-bar">
        <input id="gemlyInput" type="text" class="gemly-input" placeholder="给晶灵留言，回车发送…" autocomplete="off" maxlength="500">
        <button id="gemlySendBtn" class="gemly-send-btn" aria-label="发送"><i class="fa fa-paper-plane"></i></button>
    </footer>
</aside>
<div id="gemlyDrawerBackdrop" class="gemly-drawer-backdrop" aria-hidden="true"></div>

<style>
    /* 完整样式见各页面已集成代码：樱花粉白主题、420px抽屉、60px标题栏、72px输入栏、气泡、loading动画 */
</style>

<script>
/* 完整逻辑见各页面已集成代码：配置区 + 滑入动画 + 消息渲染 + 演示模式/真实API双通路 */
</script>
<!-- ============ /Gemly AI 对话抽屉组件 ============ -->
```

> 完整代码（含全部 CSS 与 JS）已集成在 [index.html](file:///c:/Users/陈烨/Desktop/互联网创新/demo1/index.html#L583-L889)，可直接复制该块到其他页面。

---

## 七、后端代理接口实现要求

### 7.1 接口契约

| 项 | 值 |
|---|---|
| URL | `GEMLY_PROXY_URL`（默认 `/api/gemly-chat`） |
| Method | `POST` |
| Content-Type | `application/json` |

### 7.2 请求体（前端发给后端）

```json
{
  "agent_id": "智能体ID",
  "message": "用户输入文本",
  "history": [
    { "role": "user", "content": "历史用户消息" },
    { "role": "assistant", "content": "历史AI回复" }
  ]
}
```

### 7.3 响应体（后端返回前端）

```json
{
  "reply": "AI回复文本"
}
```

### 7.4 后端伪代码示例（Python Flask）

```python
import os, requests
from flask import Flask, request, jsonify

app = Flask(__name__)
COZE_PAT = os.environ.get('COZE_PAT')      # pat_令牌只存后端环境变量
COZE_API = 'https://api.coze.cn/open_api/v2/chat'

@app.post('/api/gemly-chat')
def gemly_chat():
    data = request.json
    # 携带PAT调用Coze开放API(具体字段以Coze官方文档为准)
    resp = requests.post(COZE_API,
        headers={'Authorization': f'Bearer {COZE_PAT}', 'Content-Type': 'application/json'},
        json={'bot_id': data['agent_id'], 'query': data['message'],
              'conversation_id': '', 'user': 'web_user'},
        timeout=30)
    reply = resp.json().get('messages', [{}])[-1].get('content', '')
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(port=3000)
```

> ⚠️ 以上为示例，Coze API 字段请以 [Coze 开放平台文档](https://www.coze.cn/open) 为准。PAT 令牌通过环境变量注入，**绝不硬编码**。

---

## 八、已集成页面清单

以下 15 个业务页面已集成 Gemly AI 对话组件（状态：✅ 完成）：

| 序号 | 页面文件 | 路径 | 状态 |
|---|---|---|---|
| 1 | 首页 | `index.html` | ✅ |
| 2 | 产品列表 | `products.html` | ✅ |
| 3 | 产品详情 | `product-detail.html` | ✅ |
| 4 | 品牌故事 | `our-story.html` | ✅ |
| 5 | 价值理念 | `our-values.html` | ✅ |
| 6 | 博客首页 | `blog.html` | ✅ |
| 7 | 博客详情 | `blog-detail.html` | ✅ |
| 8 | 资源中心 | `resources.html` | ✅ |
| 9 | DIY 定制 | `diy.html` | ✅ |
| 10 | 联系我们 | `contact.html` | ✅ |
| 11 | 常见问题 | `faq.html` | ✅ |
| 12 | 购物车 | `cart.html` | ✅ |
| 13 | 用户账户 | `account.html` | ✅ |
| 14 | 注册登录 | `zuce.html` | ✅ |
| 15 | 404 错误页 | `404.html` | ✅ |

**未集成的页面**（备用模板，按规范保留）：`demo1.html`、`new_file.html`

---

## 九、移动端适配说明

### 9.1 响应式断点

| 屏幕 | 抽屉宽度 | 遮罩行为 |
|---|---|---|
| PC（>640px） | 固定 420px | 透明不阻挡主体浏览 |
| 移动端（≤640px） | 100vw 全屏 | 半透明遮罩，点击关闭 |

### 9.2 viewport 要求

确保页面 `<head>` 已设置 viewport meta：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 9.3 输入框移动端体验

- 输入框 `font-size: 14px`（≥16px 会触发 iOS 自动放大，14px 平衡可读性与不缩放）
- 发送按钮 44×44px，符合移动端触控热区标准
- 抽屉打开时 `body.overflow = hidden`，防止背景滚动

---

## 十、本地调试注意事项

### 10.1 演示模式调试

1. 保持 `GEMLY_DEMO_MODE = true`
2. 本地起 HTTP 服务器（如 `python -m http.server 8080`）
3. 访问 `http://localhost:8080/index.html`
4. 点击右下角紫色按钮 → 抽屉滑入 → 输入文字 → 回车发送 → 观察模拟回复

### 10.2 真实 API 调试

1. 改 `GEMLY_DEMO_MODE = false`
2. 填入 `GEMLY_AGENT_ID`
3. 启动后端代理服务（如 Flask 监听 3000 端口）
4. 设置 `GEMLY_PROXY_URL = 'http://localhost:3000/api/gemly-chat'`
5. 后端环境变量注入 `COZE_PAT=pat_xxxxx`
6. F12 Network 面板观察请求/响应

### 10.3 常见问题

| 问题 | 原因 | 解决 |
|---|---|---|
| 点击按钮无反应 | 按钮未设 `id="openGemlyAiBtn"` | 检查按钮 id |
| 抽屉不滑入 | JS 报错导致中断 | F12 控制台查错 |
| 真实模式返回网络错误 | 后端未启动 / CORS 未配置 | 启动后端，配置 CORS 允许前端域名 |
| 模拟回复不变 | 演示模式随机池较小 | 正常现象，上线用真实 API |
| 移动端抽屉不全屏 | viewport meta 缺失 | 添加 viewport meta 标签 |

---

## 十一、UI 视觉规范对照

| 规范项 | 实现 |
|---|---|
| 樱花粉主色 #FFD1DC | ✅ 用户气泡、发送按钮、标题栏图标 |
| 粉白底色 #FFF8FA | ✅ 抽屉背景、输入框背景 |
| AI 气泡纯白 #FFFFFF + 浅粉描边 | ✅ `border: 1px solid #FFE0EC` |
| 标题栏渐变 #FFF0F5→#FFE6EF | ✅ `linear-gradient(180deg, #FFF0F5, #FFE6EF)` |
| 正文 #444444 / 标题 #222222 | ✅ |
| 大圆角 14px | ✅ 气泡圆角 14px，输入框 22px |
| 顶部标题栏 60px | ✅ `height: 60px` |
| 底部输入栏 72px | ✅ `height: 72px` |
| 移除 Coze/扣子所有标识 | ✅ 全自研界面，零第三方 UI |

---

## 十二、版本变更记录

| 版本 | 日期 | 变更说明 |
|---|---|---|
| v1.0 | 2026-08-07 | iframe 嵌入 Coze 商店页面（已废弃） |
| v2.0 | 2026-08-09 | 自研樱花粉白对话 UI + 后端代理架构 + 演示模式开关，移除 iframe，PAT 令牌仅存后端 |

---

**文档维护**：Haven Gems 项目组
**安全提醒**：pat_ 令牌属于密钥，只能存放后端服务，严禁写入前端代码或提交 Git
