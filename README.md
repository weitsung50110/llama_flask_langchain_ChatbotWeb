# nlp_ollama_flask
Using ollama nlp LLM to combine with flask to let the LLM can be shown on web.

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

- 若想要單獨使用ollama看看可以輸入

      ollama run llama3

#### 4. 若想要使用ollama和flask結合的web網頁版nlp llm功能，請先進入 /app/flask 當中

    cd /app/flask

#### 5. 會在/flask資料夾下面看到app2.py，直接輸入以下指令

    python3 app2.py

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

