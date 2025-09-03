# TransNative - 地道英语翻译工具

TransNative 是一个使用大语言模型（LLM）进行中文到地道美式英语翻译的工具。与传统翻译软件不同，它提供多种美国人日常生活中使用的表达方式，让翻译结果更加自然和地道。

## 快速开始

Windows用户可以直接运行 `start.bat` 脚本来启动应用，该脚本会自动启动后端和前端服务。

或者按照以下步骤手动启动：

## 功能特点

- 中文翻译成多种地道的美式英语表达
- 使用豆包最新模型提供高质量翻译，豆包Pro模型作为备选
- 简洁易用的Web界面
- 支持多种翻译选项，满足不同语境需求
- 翻译结果包含使用场景和对象说明，避免误用

## 技术架构

- 后端：FastAPI (Python)
- 前端：HTML + JavaScript
- 翻译引擎：DeepSeek API（首选）+ DeepSeek Pro API（备选）

## 安装与运行

1. 克隆项目代码：
   ```bash
   git clone <repository-url>
   cd TransNative
   ```

2. 创建虚拟环境并安装依赖：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或 venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   在 `.env` 文件中设置你的 API 密钥：
   ```bash
   # DeepSeek API配置
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   DEEPSEEK_ENDPOINT=https://api.deepseek.com/chat/completions
   ```

4. 运行应用：
   ```bash
   # 方法1: 使用启动脚本(Windows)
   start.bat
   
   # 方法2: 分别启动服务
   python main.py
   # 在另一个终端中运行:
   # python -m http.server 8001
   ```

5. 访问应用：
   打开浏览器访问 `http://localhost:8001` 查看前端界面
   API 文档可以在 `http://localhost:8000/docs` 查看

## API 接口

### 翻译接口

- **URL**: `/translate`
- **方法**: POST
- **请求参数**:
  ```json
  {
    "text": "要翻译的中文文本"
  }
  ```
- **响应**:
  ```json
  {
    "translations": [
      "地道的英语翻译1",
      "地道的英语翻译2",
      "地道的英语翻译3"
    ]
  }
  ```

## 部署

可以使用以下方式部署应用：

1. 使用 Docker (推荐)
2. 部署到云服务器
3. 使用云函数服务（如 Vercel、Netlify 等）

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 许可证

[MIT License](LICENSE)