# procon34_api
コマンドライン上での操作は全て Powershell 上で行ってください
## 事前準備
このレポジトリのダウンロード & 解凍
```Python
レポジトリ右上 Code から zip でダウンロードしてどこかに展開して Powershell でその場所に移動してください
./server 下でしか動かさないので カレントディレクトリを このレポジトリ/server になるように移動してください
```
Streamlit のインストール  
実行する場所は関係ないのでどこでもいいです
```Python
>>> pip install streamlit
```
## Run
initial.json の構成で 0秒 でサーバーを建てる
```Python
>>> cd ./server
>>> .\procon-server_win -c initial.json -start 0
```
streamlit の gui サーバーを建てる
```Python
>>> cd ./server
>>> streamlit run gui.py

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.33:8501
勝手にブラウザに移動します
.
.
.
```
もちろん streamlit 上でデバック等できるようにしてますが、コマンドライン上 ( streamlit run gui.py したほう ) でも確認ができます

## 使い方  
めんどくさいので自分でいろいろ試してください
