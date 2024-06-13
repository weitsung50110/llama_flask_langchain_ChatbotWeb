# ollama_flask_langchain_web
Using ollama nlp LLM to combine with flask to let the LLM can be shown on web. Using LLM as your personal assistant.

我們將介紹如何使用Ollama LLM結合Flask來構建一個聊天機器人chat bot網站。本教學將會使用Llama3作為我們的LLM，並且採用LangChain, , JavaScript, Jinja2和Tailwind CSS框架，確保你在任何設備上都能獲得最佳的響應式設計（RWD）體驗。

## 目錄Table of Contents
- [Website Features Overview](#Website-Features-Overview)
- [Dockers](#Dockers)
- [Code Explanation](#Code-Explanation)
- [Server-Sent Events (SSE)](#Server-Sent-Events(SSE))

需要的套件>

    langchain_community
    langchain_core
    flask
  
## Website Features Overview
### Main page
At the main page you can see the beautiful logo I made, because I use Llama3 as LLM, so I put a llama in the middle of logo.😝

![](https://github.com/weitsung50110/ollama_flask_langchain_web/blob/main/github_imgs/00.png)

### Navigation bar
You can connect to all my resources, you can find me on linkdin, medium and github.

![](https://github.com/weitsung50110/ollama_flask_langchain_web/blob/main/github_imgs/2.png)

### Input area

![](https://github.com/weitsung50110/ollama_flask_langchain_web/blob/main/github_imgs/4.png)

### Asking llama3 questions
    Who are you?
    
![](https://github.com/weitsung50110/ollama_flask_langchain_web/blob/main/github_imgs/1.png)
    Do you love me?
    
![](https://github.com/weitsung50110/ollama_flask_langchain_web/blob/main/github_imgs/3.png)

### Timestamp
![](https://github.com/weitsung50110/ollama_flask_langchain_web/blob/main/github_imgs/6.png)

## Docker
#### 1. 先去把image pull下來

    docker pull weitsung50110/ollama_flask

weitsung50110/ollama_flask裡面我已經把ollama和flask都安裝完成了，並把llama3和llama2也已經安裝在本地了。

#### 2. Run image in order to generate container
 ~/trans_project掛載到容器內的app資料夾下面， ~/trans_project是在ubuntu中的寫法，若你是windows請自行更改並創建資料夾。

        docker run -d \
        -v ollama:/root/.ollama \
        -v ~/trans_project:/app \
        -p 5066:5000 \
        -p 11466:11434 \
        --name ollama_flask \
        weitsung50110/ollama_flask:1.0

#### **Port端口 -p 講解教學 很重要**
在 Docker 的端口映射語法 `-p <host_port>:<container_port>` 中： <br />
- `<host_port>` 是主機上的端口號。 <br />
- `<container_port>` 是容器內部的端口號。
 
因為ollama的docker image預設port端口是11434，<br />
所以我將主機的 11466 端口映射到ollama容器的 11434 端口。

因為flask的docker image預設port端口是5000，<br />
所以我將主機的 5066 端口映射到flask容器的 5000 端口。

`5066` 是主機上的端口號。這是你用來從外部（例如你的瀏覽器或其他網絡工具）訪問應用程序的端口。<br />
`5000` 是容器內部應用程序運行的端口。這是應用程序在容器內部綁定和監聽的端口。

這樣配置後，當你訪問 127.0.0.1:5066（假設你的 Docker 主機是本地主機）時，實際上是通過主機的 5066 端口進入容器的 5000 端口，從而訪問flask容器內部運行的應用程序LLM。

當你訪問 127.0.0.1:11466，可以看到`Ollama is running`的字樣。

#### 3. 進入ollama_flask容器conatiner裡面

        docker exec -it ollama_flask /bin/bash

- 請一定要先輸入以下指令

      ollama run llama3

> **_如果你沒有先把llama3安裝在container裡面的話，flask會無法打開_**

#### 4. 若想要使用ollama和flask結合的web網頁版nlp llm功能，請先進入 /app/flask 當中

    cd /app/flask

#### 5. 會在/flask資料夾下面看到app.py，直接輸入以下指令

    python3 app.py

#### 一定要指定port，1個container可以指定多個port
如果你docker run的時候沒有輸入-p xxxx:5000 去指定port，這樣就會無法用127.0.0.1:xxxx來連進flask裡面，
- <h4>所以run的時候一定要指定port。</h4>

錯誤範例 >> 
docker run -d 
-v ollama:/root/.ollama 
-v ~/trans_project:/app 
~~-p 5066:5000~~ 
-p 11466:11434 
--name ollama_flask 
weitsung50110/ollama_flask:1.0

#### 6. 跑成功就可以看到print以下畫面
print出來的字串為Running on `127.0.0.1:5000`或`172.17.0.2:5000`，但**主要以你docker run指定的port為準**，<br />
若你的port指定-p 5066:5000，就要輸入 `127.0.0.1:5066`才能連進去唷~

    root@4be643ba6a94:/app/flask# python3 app2.py
     * Serving Flask app 'app2'
     * Debug mode: on
    INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:5000
     * Running on http://172.17.0.2:5000
    INFO:werkzeug:Press CTRL+C to quit
    INFO:werkzeug: * Restarting with watchdog (inotify)
    WARNING:werkzeug: * Debugger is active!
    INFO:werkzeug: * Debugger PIN: 285-152-236

![](https://github.com/weitsung50110/ollama_flask_langchain_web/blob/main/github_imgs/5.png)

## Code Explanation
#### Server
你在資料集中的app.py，也就是server看到render_template代表要渲染網頁了，這時我有把一些值傳到index.html網頁當中。

    return render_template('index.html', query_input=query_input, output=output)

- query_input : 使用者詢問LLM所輸入的問題
- output : LLM的回應
#### Web
Jinja2 提供了一些強大的模板語法，讓我們可以在 HTML 文件中使用 Python 風格的控制結構。

可以看到我在html藉由jinja2使用條件判斷。

    <div class="mt-6">
        {% if query_input %}
        <div class="bg-gray-100 p-4 rounded mb-4">
            <p class="text-gray-700">{{ query_input }}</p>
        </div>
        {% endif %}
        {% if output %}
        <div class="bg-gray-100 p-4 rounded">
            <p class="text-gray-700">{{ output }}</p> <!-- Use the safe filter to render HTML from output -->
        </div>
        {% endif %}
    </div>

接下來我們將探討 Jinja2 模板語法中的控制結構，特別是條件判斷和迴圈語法，我舉幾個簡單的例子給大家，。

#### Jinja2 模板語法
Jinja2 提供了一些強大的模板語法，讓我們可以在 HTML 文件中使用 Python 風格的控制結構。以下是一些常用的控制結構：

1. 條件判斷（{% if %}）

條件判斷允許我們根據變數的值來決定是否渲染某些內容。

    {% if condition %}
        <!-- 當條件為真時渲染這段內容 -->
    {% elif other_condition %}
        <!-- 當另一個條件為真時渲染這段內容 -->
    {% else %}
        <!-- 當所有條件都不成立時渲染這段內容 -->
    {% endif %}

2. 迴圈（{% for %}）

迴圈允許我們遍歷列表或其他可迭代對象，並渲染每個元素。

    {% for item in items %}
        <!-- 渲染每個 item 的內容 -->
    {% endfor %}
    3. 範圍迴圈（{% for i in range(start, end) %}）

我們也可以使用範圍迴圈來遍歷一個數字範圍：

    {% for i in range(1, 11) %}
        <p>數字：{{ i }}</p>
    {% endfor %}
    
在 Jinja2 模板語法中，所有的控制結構（如條件判斷和迴圈）都**必須以相應的 {% end %} 語句來結束**。這是為了明確定義控制結構的範圍，避免代碼混淆。

我們可以看到 if 條件判斷用 {% endif %} 結束，for 迴圈用 {% endfor %} 結束。這些結束標記是必不可少的，否則模板引擎會無法正確解析模板，並且會拋出錯誤。

## Server-Sent Events(SSE)
#### 生成器函數 generate() 詳解：
    def generate():
    while True:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 取得當前時間並格式化
        data = f"data: {current_time}\n\n"  # 根據SSE格式要求構建數據字符串
        yield data  # 通過生成器返回數據給調用者（客戶端）
        time.sleep(1)  # 每秒推送一次數據

* `generate()` 函數使用了一個無窮循環 (`while True`)，每次循環都取得當前時間 (`datetime.now()`)，並將其格式化為 `%Y-%m-%d %H:%M:%S` 的字串形式。
* 使用 `f-string` 將格式化後的時間插入到 `data` 字串中，並按照 SSE 的規範構建數據。
* 通過 `yield` 返回 `data` 給調用者（客戶端），使得生成器可以被迭代並逐步返回新的數據。
* `time.sleep(1)` 使生成器每秒鐘推送一次數據，實現即時更新效果。

#### SSE 路由 (/stream) 的設置：

    @app.route('/stream')
    def stream():
        return Response(generate(), mimetype='text/event-stream')

在 Flask 應用中設置 `/stream` 路由，當客戶端訪問該路由時，會返回一個 `Response` 對象，其內容由 `generate()` 函數生成，
並設置 `mimetype='text/event-stream'` 以指定這是一個 SSE 流。

#### JavaScript 說明：

    <script>
        const eventSource = new EventSource('/stream');
                
        eventSource.onmessage = function(event) {
            document.getElementById('datetime').innerHTML = event.data;
        };
    </script>

1\. `const eventSource = new EventSource('/stream');` 
* `EventSource` 是 HTML5 中引入的一種 API，它允許網頁從服務器端接收推送的事件。
* `new EventSource('/stream')` 創建了一個新的 `EventSource` 對象，並指定了要訂閱的服務器端端點 `/stream`。
這意味著客戶端將會向 `/stream`發送一條新的事件消息時，JavaScript 會自動觸發 `onmessage` 事件處理器函數。

2\. `eventSource.onmessage = function(event) { ... };` 
* 一旦客戶端訂閱成功，當服務器端向 `/stream` 發送一條新的事件消息時，JavaScript 會自動觸發 `onmessage` 事件處理器函數。
* `event` 參數包含了從服務器端發送來的事件消息的相關信息，包括數據內容。

3\. `document.getElementById('datetime').innerHTML = event.data;` 
* 在 `onmessage` 事件處理器函數內部，這行代碼將服務器端發送來的數據 `event.data` 更新到 HTML 文檔中具有 `id="datetime"` 的元素內。
* 通常情況下，`event.data` 是一段文本數據，它包含了服務器端發送的即時信息，例如時間戳、消息內容等。

#### 工作流程： 
* 當頁面加載時，JavaScript 代碼會創建一個 `EventSource` 對象，並發起對 `/stream` 的 HTTP GET 請求。
* 一旦服務器端有新的事件消息到來，它會將該消息推送到所有訂閱了 `/stream` 的客戶端（即這裡的網頁）。
* 客戶端接收到來自服務器端的事件消息後，透過 `onmessage` 事件處理器函數將消息內容更新到 HTML 中的指定元素（這裡是 `id="datetime"` 的元素）。

樣就實現了一個基本的 SSE 客戶端，用於接收服務器端推送的事件消息並即時更新到網頁上。

更詳細內容請看medium教學 >> [利用Ollama LLM、Flask、LangChain實作聊天機器人chat bot網站](https://medium.com/@weiberson/%E5%88%A9%E7%94%A8ollama-llm-flask-langchain%E5%92%8Ctailwind-css%E5%AF%A6%E4%BD%9C%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BAchat-bot%E7%B6%B2%E7%AB%99-b98a891977e8#5083).
