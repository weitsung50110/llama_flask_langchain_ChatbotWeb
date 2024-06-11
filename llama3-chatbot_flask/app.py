from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from flask import Flask, request, render_template
import logging
import re

# 設定基本的日誌記錄
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("watchdog").setLevel(logging.WARNING) #設置 watchdog 的日誌級別，將其設置為 WARNING，只有級別為 WARNING 或更高的日誌信息才會被記錄，從而避免顯示大量的調試（DEBUG）信息

# 創建 Flask 應用程式
app = Flask(__name__)

# 初始化 OpenAI 語言模型和輸出解析器
llama_model = Ollama(model="llama3")


'''這種寫法是Python中的類繼承（class inheritance）。在這個例子中，MyOutputParser 類別繼承自 StrOutputParser 類別。這意味著 MyOutputParser 將擁有 StrOutputParser 的所有屬性和方法，同時也可以根據需要添加新的屬性和方法。'''
'''def parse 方法被隱式地呼叫了。Langchain設定def為 parse才會進去def，若設成其他名稱 則不會進入，可以用"name"+txt，看看name會不會出現在前面來測試。'''
'''若沒特別指定def parse，回傳方法則會使用預設，所以Lotus : 就會不見ㄌ'''
class MyOutputParser(StrOutputParser):
    def parse(self, text):
        text = "AI : " + text
        return text

text_sys = "You are my personal assistant"

# 定義初始化聊天機器人的函數
def initialise_llama3(text_sys):
    try:
        # 創建聊天機器人的提示模板
        create_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", f"{text_sys}"),  # 設定系統訊息，描述機器人的角色
                ("user", "Question: {question}")  # 定義使用者訊息，包含一個變數 {question}
            ]
        )

        format_output = MyOutputParser()

        # 創建處理管道
        chatbot_pipeline = create_prompt | llama_model | format_output
        return chatbot_pipeline
    except Exception as e:
        logging.error(f"Failed to initialize chatbot: {e}")
        raise



# 定義首頁路由
@app.route('/', methods=['GET', 'POST'])
def main():
    query_input = None
    output = None
    text_sys = "You are my personal assistant"

    if request.method == 'POST':
        query_input = request.form.get('query-input')
        
        # 初始化聊天機器人
        chatbot_pipeline = initialise_llama3(text_sys) 

        if query_input:
            try:
                # 調用聊天機器人處理查詢
                response = chatbot_pipeline.invoke({
                    'question': query_input,
                    'text_sys': text_sys
                })
                output = response
            except Exception as e:
                logging.error(f"Error during chatbot invocation: {e}")
                output = "Sorry, an error occurred while processing your request."
    
    return render_template('index.html', query_input=query_input, output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
