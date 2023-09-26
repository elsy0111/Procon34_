import streamlit as st
from copy import deepcopy as dc
from datetime import datetime

import requests as rq
import json

# url = "https://www.procon.gr.jp/"
url = "http://127.0.0.1:3000/"
# api_token = "ariakee5d5af0c7ad9401b6449eda7ee0e8730f24f77d5b6da2ac615aca3c1f4"
api_token = "abc12345"
# header = {"procon-token" : api_token}
header = {"Content-Type" : "application/json",
           "procon-token" : api_token}

# 試合一覧取得API
# 参加する試合の一覧を取得するAPIです

# Require : token
# Response { [
#            int    id,                 試合ID                  (0 <= id)
#            int    turns,              試合の総ターン数        (30 <= turns <= 200)
#            int    turnSeconds,        １ターン当たりの秒数    (3 <= turnSeconds <= 15)

#            bonus  {                   得点の係数
#            int    wall: 10,           城壁係数        (const 10)
#            int    territory : 30,     陣地係数        (const 30)
#            int    castle : 100        城係数          (const 100)
#                   }

#            board  { 
#            int    width,              横              (11 <= width <= 25)
#            int    height,             縦              (11 <= height <= 25)
#            int    mason,              職人の数        (2 <= mason <= 6)
#            Arrint structures,         構造物          (0 : なし, 1 : 池, 2 : 城)
#            Arrint masons              職人            (0 < masons: 自チーム, 0 > masons: 相手チーム)
#                   }

#            string opponent,           相手のチーム名
#            bool   first               自チームが先手かどうか
#            ] }

def get_matches(Match_Number : int):
    Match_Number = int(Match_Number)
    r = rq.get(url + "matches", headers = header)
    response = r.json()
    status_code = r.status_code
    print("get_match status_code :", r.status_code)
    if (Match_Number == -1):
        return response["matches"], status_code
    else:
        return response["matches"][Match_Number], status_code

# res = get_matches()
# ID = res['id']
# cout(res)
# print(ID)

# N = res['board']['mason']
# print(N)

# 試合状態取得API
# 試合の状態を取得するAPIです

# Require : token, id
# Response { 
#            int    id,                 試合ID                  (0 <= id)
#            int    turn,               どのターンのボードか    (0 <= turn <= turns)

#            board  {
#            Arrint walls,              城壁の情報      (0 : なし, 1 : 自チーム, 2 : 相手チーム の城壁)
#            Arrint territories,        陣地の情報      (0 : 中立, 1 : 自チーム, 2 : 相手チーム, 3 : 両チーム の陣地)
#            int    width,              横              (11 <= width <= 25)
#            int    height,             縦              (11 <= height <= 25)
#            int    mason,              職人の数        (2 <= mason <= 6)
#            Arrint structures,         構造物          (0 : なし, 1 : 池, 2 : 城)
#            Arrint masons              職人            (0 < masons: 自チーム, 0 > masons: 相手チーム)
#                   }

#            logs { [
#            int    turn,               実施ターン          (1 <= turn <= turn)
#                   actions { [
#                   bool    succeeded,  行動が成功したか    (true : 成功, false : 失敗)
#                   int     type,       行動タイプ          (0 : 滞在,  1 : 移動　, 2 : 建築, 3 : 解体)
#                   int     dir         方向(左上を(1, 1))  (1 : 左上,  2 : 上　　, 3 : 右上, 
#                           ] }                              8 : 左　,  0 : 無方向, 4 : 右　, 
#                   ] }                                      7 : 左下,  6 : 下　　, 5 : 右下)
#
#           }

def get_matching(id : int):
    r = rq.get(url + "matches/" + str(id), headers = header)
    response = r.json()
    status_code = r.status_code
    print("get_matching status_code :", r.status_code)
    return response, status_code


# 行動計画更新API
# 現在のターンに対する行動計画を更新するAPIです

# Require : token, id
# Response  { 
#            int    turn,        行動を計画するターン    (0 <= turn(次のターンのみ) <= 200)
#            actions { [
#            int     type,       行動タイプ          (0 : 滞在,  1 : 移動　, 2 : 建築, 3 : 解体)
#            int     dir         方向(左上を(1, 1))  (1 : 左上,  2 : 上　　, 3 : 右上, 
#                   ] }                               8 : 左　,  0 : 無方向, 4 : 右　, 
#           }                                         7 : 左下,  6 : 下　　, 5 : 右下)

def post_actions(id : int, masons : int, turn : int, type : int, direction : int):
    actions = {
            'turn' : turn, 
            'actions' : [
                {
                    'type' : type, 
                    'dir' : direction
                }, 
                {
                    'type' : type, 
                    'dir' : direction
                }
            ]
        }
    r = rq.post(url + "matches/" + str(id), headers = header, data = json.dumps(actions))
    print("post_actions status_code :", r.status_code)


def simple_get_matches(res : json):
    Res = dc(res)

    structures_arr = Res["board"]["structures"]
    masons_arr = Res["board"]["masons"]

    Res["board"]["structures"] = []
    Res["board"]["masons"] = []
    for i in structures_arr:
        Res["board"]["structures"].append(str(i))
    for i in masons_arr:
        Res["board"]["masons"].append(str(i))

    return Res

def simple_get_matching(res : json):
    Res = dc(res)
    del Res["logs"]

    structures_arr = Res["board"]["structures"]
    masons_arr = Res["board"]["masons"]
    walls_arr = Res["board"]["walls"]
    territories_arr = Res["board"]["territories"]

    Res["board"]["structures"] = []
    Res["board"]["masons"] = []
    Res["board"]["walls"] = []
    Res["board"]["territories"] = []
    for i in structures_arr:
        Res["board"]["structures"].append(str(i))
    for i in masons_arr:
        Res["board"]["masons"].append(str(i))
    for i in walls_arr:
        Res["board"]["walls"].append(str(i))
    for i in territories_arr:
        Res["board"]["territories"].append(str(i))

    return Res

def page1():

    st.title("GET")

    if "status_code" not in st.session_state:
        st.session_state.status_code = "Status(None)"
    if "res" not in st.session_state:
        st.session_state.res = "Res(None)"
    if "res_fmt" not in st.session_state:
        st.session_state.res_fmt = "Res_fmt(None)"
    if "logs" not in st.session_state:
        st.session_state.logs = ""

    Get_Matches = st.button("Get_Matches")
    if Get_Matches:
        st.session_state.res, st.session_state.status_code = get_matches(st.session_state["Match_Number"])
        if (st.session_state["Match_Number"] == "-1"):
            st.session_state.res_fmt = "None"
        else:
            st.session_state.res_fmt = simple_get_matches(st.session_state.res)
        st.session_state.logs = ""

    Get_Matching = st.button("Get_Matchng")
    if Get_Matching:
        st.session_state.res, st.session_state.status_code = get_matching(st.session_state["ID"])
        try:
            st.session_state.res_fmt = simple_get_matching(st.session_state.res)
            st.session_state.logs = st.session_state.res["logs"]
        except:
            None

    st.text_input("Match_Number", "-1", key="Match_Number")
    st.text_input("ID", key="ID")

    st.write("Status Code :", st.session_state.status_code, datetime.now())
    st.write("Raw :  ", st.session_state.res)
    st.write("Simple : ", st.session_state.res_fmt)
    st.write("Logs : ", st.session_state.logs)

def page2():
    st.title("POST")

    st.text_input("ID", key="ID")
    st.text_input("Masons", key="Masons")
    st.text_input("Turn", key="Turn")
    st.text_input("Actions [[turn, direction], ...]", key="Actions")

    st.write("Status Code :", st.session_state.status_code)

def page3():
    st.title("VIS")

pages = dict(
    page1="GET",
    page2="POST",
    page3="VIS",
)

page_id = st.sidebar.selectbox( # st.sidebar.*でサイドバーに表示する
    "Change",
    ["page1", "page2", "page3"],
    format_func=lambda page_id: pages[page_id], # 描画する項目を日本語に変換
)

if page_id == "page1":
    page1()

if page_id == "page2":
    page2()

if page_id == "page3":
    page3()

