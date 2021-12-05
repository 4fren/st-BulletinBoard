import streamlit as st
import streamlit.components.v1 as stc
import datetime
import hashlib
import random
from google.oauth2 import service_account
from gsheetsdb import connect
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"],scopes=["https://www.googleapis.com/auth/spreadsheets"])
key_dict = {
    "type": st.secrets["gcp_service_account"]["type"],
    "project_id": st.secrets["gcp_service_account"]["project_id"],
    "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
    "private_key": st.secrets["gcp_service_account"]["private_key"],
    "client_email": st.secrets["gcp_service_account"]["client_email"],
    "client_id": st.secrets["gcp_service_account"]["client_id"],
    "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
    "token_uri": st.secrets["gcp_service_account"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
}
credentials2 = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
con = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(allow_output_mutation=True, ttl=5)
def run_query(query):
    rows = con.execute(query, headers=1)
    return rows

def make_hashes(password):
    	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

@st.cache(allow_output_mutation=True)
def cache_list2():
    lst = []
    return lst

@st.cache(allow_output_mutation=True)
def cache_list_pageFlag():
    lst = []
    lst.append(0)
    return lst

@st.cache(allow_output_mutation=True)
def cache_list_writing():
    lst = []
    return lst

@st.cache(allow_output_mutation=True)
def cache_list_thread():
    lst = []
    return lst

@st.cache(allow_output_mutation=True)
def cache_list_thread2():
    lst = []
    return lst

@st.cache(allow_output_mutation=True)
def cache_list_password():
    lst = []
    return lst

@st.cache(allow_output_mutation=True)
def cache_list_translate():
    lst = []
    return lst

def word_list():
    wordList = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0"]
    lst = []
    for i in range(0,8,1):
        j = random.randrange(len(wordList))
        lst.append(wordList[j])
    return lst

def saveToSpreadsheet(wks,threadLen,thread,d_today,secret,key):
    row_list = [thread,d_today.strftime('%Y-%m-%d'),secret,key,threadLen]
    wks.insert_row(row_list,index=threadLen+2)
    #wks.update_cell(threadLen + 2, 1, thread)
    #wks.update_cell(threadLen + 2, 2, d_today.strftime('%Y-%m-%d'))
    #wks.update_cell(threadLen + 2, 3, secret)
    #wks.update_cell(threadLen + 2, 4, key)
    #wks.update_cell(threadLen + 2, 5, threadLen + 2)

def sendThread(thread,secret,threadLen,gc):
    #入力欄が空でなければデータベースに書き込み
    if thread != "":
        d_today = datetime.date.today()

        wks = gc.open('pyStreamlitBulletinboard').sheet1

        if secret == True:
            k = word_list()
            key = ""
            for i in range(0,len(k),1):
                key += k[i]
            hashed_key = make_hashes(key)

            saveToSpreadsheet(wks,threadLen,thread,d_today,secret,hashed_key)

            st.subheader("このスレッドのパスワード")
            st.info(key)
            st.write("注意：一度しか表示されません。忘れないようにしてください。")
        
        elif secret == False:
            key = ""

            saveToSpreadsheet(wks,threadLen,thread,d_today,secret,key)

    else:
        st.warning("未入力です")

def main():
    pageFlag = cache_list_pageFlag()

    selectedThread = cache_list_thread()

    selectedThread2 = cache_list_thread2()
    
    sheet_url = st.secrets["private_gsheets_url"]

    gc = gspread.authorize(credentials2)
    
    st.sidebar.write('匿名！ 登録なし！\n\nシンプルな掲示板サイト')
    
    if pageFlag[0] == 0:
        

        selectedThread2.clear()

        rows = run_query(f'SELECT * FROM "{sheet_url}"')

        threadLen = 0
        # Print results.
        for row in rows:
            #st.write(f"{row.name} has a :{row.pet}:")
            threadLen = threadLen + 1
            #selectedThread2.append((row.スレッドタイトル,row.投稿日時,row.鍵フラグ,row.パスワード))
        #print(selectedThread2)
        #print(threadLen)
        #threadLen = len(selectedThread2)
        print(threadLen)

        #タイトル
        st.title("掲示板")

        html_style1 = """
        <style>
        #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div:nth-child(9) > div > div:nth-child(1) > div:nth-child(1) > div > div > button
        {
            margin-left: 85%;
        }

        #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div:nth-child(9) > div > div:nth-child(2) > div:nth-child(1) > div > div > button
        {
            margin-left: 50%;
        }

        #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div:nth-child(8) > div > label > span
        {
            margin-left: 69%;
        }

        #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div.css-1xb5r1o.epcbefy1 > div:nth-child(1) > div:nth-child(1) > div > div > button
        {
            margin-left: 83%;
        }
        </slyle>
        """

        st.markdown(html_style1,unsafe_allow_html=True)

        if 'count' not in st.session_state: 
            st.session_state.count = 0 #countがsession_stateに追加されていない場合，0で初期化

        ta_placeholder = st.empty()

        secret = st.checkbox("閲覧に制限をかける🔑🔒",False)

        col_clear,col_text_area = st.columns([4,1])

        with col_clear:
            if st.button('クリア'):
                st.session_state.count += 1

        #入力欄
        thread = ta_placeholder.text_area('スレッド作成', value='', key=st.session_state.count)

        with col_text_area:
            # Every form must have a submit button.
            submitted = st.button("作成")
        
        if submitted:
            sendThread(thread,secret,threadLen,gc)

        html_style2 = """
        <style>
        #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div.css-1mg5w7t.epcbefy1 > div:nth-child(1) > div:nth-child(1) > div > div > button
        {
            margin-left: 83%;
        }

        #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div.css-1mg5w7t.epcbefy1 > div:nth-child(1) > div.css-1etojpn.e1tzin5v3 > div > div:nth-child(2) > div:nth-child(1) > div > div > div > button
        {
            
        }
        </slyle>
        """

        st.markdown(html_style2,unsafe_allow_html=True)

        #nn = threadAmount()

        selectedThread2.clear()

        #sheet_url = st.secrets["private_gsheets_url"]
        rows = run_query(f'SELECT * FROM "{sheet_url}"')

        threadLen = 0
        # Print results.
        for row in rows:
            #st.write(f"{row.name} has a :{row.pet}:")
            threadLen = threadLen + 1
            selectedThread2.append((row.スレッドタイトル,row.投稿日時,row.鍵フラグ,row.パスワード,row.ID))
        print(selectedThread2)
        #threadLen = len(selectedThread2)
        print(threadLen)

        nn = threadLen

        #表示数
        m = 10
        #ページ数
        q = (nn - 1) / m
        p = (nn - 1) % m
        if p == 0:
            qq = int(q)
        else:
            qq = int(q) + 1

        if qq < 1:
            qq = 1

        oo = nn - 10
        mm = oo + 10
        if oo < 0:
            oo = 0
        
        flagList = cache_list2()

        if nn > 0:
            with st.form('page'):
                if st.form_submit_button("再読み込み"):
                    time.sleep(3)
                    st.experimental_rerun()

                st.subheader('ページタブ')
                # カラムを追加する
                col = st.columns(qq)
                for i in reversed(list(range(0,qq,1))):
                    # コンテキストマネージャとして使う
                    with col[i]:
                        qqq = i + 1
                    
                        if st.form_submit_button(str(qqq)):
                            time.sleep(3)
                            
                            flagList.clear()
                            flagList.append(qqq)
                        
                            oo = nn - 10 * qqq
                            mm = oo + 10
                            if oo < 0:
                                oo = 0
                            print(mm,oo)

                if flagList != []:
                    oo = nn - 10 * int(flagList[0])
                    mm = oo + 10
                    if oo < 0:
                        oo = 0

                st.write(str(oo + 1) + "~" + str(mm))

                st.subheader('スレッド一覧')
                
                for i in reversed(range(oo,mm,1)):
                    #print(selectedThread2[i])

                    ii = i + 1

                    stc.html("<hr>",None,9)

                    col1,col2, col3 = st.columns([1,5,1])

                    selectedThread.clear()
                    selectedThread.append(selectedThread2[i])

                    with col1:
                        print(selectedThread)
                        st.write("<span style='font-size: 13px;'>%s</span>"%selectedThread2[i][1],unsafe_allow_html=True)
                        
                        if selectedThread2[i][2] == True:
                            st.write("🔑🔒")

                    with col2:
                        st.info(selectedThread2[i][0])

                    with col3:
                        if st.form_submit_button(str(ii) + ".".ljust(3) + "⇒"):
                            selectedThread.clear()
                            selectedThread.append(selectedThread2[i])
                            print(selectedThread)

                            pageFlag[0] = 1
                            st.experimental_rerun()
                        
            col = st.columns(qq)
            for i in reversed(list(range(0,qq,1))):
                with col[i]:
                    qqqq = i + 1
                    
                    if st.button(str(qqqq)):
                        time.sleep(3)

                        flagList.clear()
                        flagList.append(qqqq)
                        
                        oo = nn - 10 * qqqq
                        mm = oo + 10
                        if oo < 0:
                            oo = 0
                        print(mm,oo)

                        st.experimental_rerun()

    elif pageFlag[0] == 1:

        writingList = cache_list_writing()

        print(selectedThread)

        wks = gc.open('pyStreamlitBulletinboard').worksheet('シート2')
        allWriteIn = wks.get_all_values()
        print(allWriteIn)
        print(allWriteIn[1][0])
        writeInAmount = len(allWriteIn) - 1
        print(writeInAmount)

        selectedAllWriting = []
        selectedAllWritingDate = []
        for i in range(1,len(allWriteIn)):
            if int(allWriteIn[i][0]) == int(selectedThread[0][4]):
                selectedAllWriting.append(allWriteIn[i][2])
                selectedAllWritingDate.append(allWriteIn[i][3])
        print(selectedAllWriting)
        print(selectedAllWritingDate)
                
        password = cache_list_password()
        if password == []:
            password.append(0)

        st.title(selectedThread[0][0])
        
        if selectedThread[0][2] == True and password[0] != selectedThread[0][3]:
            st.subheader("鍵スレッド")
            pas = st.text_input("パスワードを入力")
            hashed_pas = make_hashes(pas)
            if st.button("決定"):
                password[0] = check_hashes(pas,hashed_pas)
                print(password)
                print(pas)
                print(selectedThread[0][3])
                if password[0] == selectedThread[0][3]:
                    st.experimental_rerun()

        else:
            st.write("<span style='font-size: 14px;'>%s</span>"%selectedThread[0][1],unsafe_allow_html=True)

            adjustmentedTalk = []

            if 'countInForm' not in st.session_state: 
                    st.session_state.countInForm = 0 #countInFormがsession_stateに追加されていない場合，0で初期化

            form_ta_placeholder = st.empty()

            col_clear, col_decide = st.columns([4,1])
            
            with col_clear:
                if st.button("クリア"):
                    st.session_state.countInForm += 1

            talk = form_ta_placeholder.text_area('書き込み', value='', key=st.session_state.countInForm)

            with col_decide:
                if st.button('書き込む'):
                    if talk != "":
                        i = 0
                        while i < len(talk):
                            adjustmentedTalk.append(talk[i])
                            if talk[i] == "\n" and talk[i - 1] != "\n" and talk[i + 1] != "\n":
                                adjustmentedTalk.append("\n")
                            i = i + 1

                        print(adjustmentedTalk)

                        i = 0
                        talk = ""
                        while i < len(adjustmentedTalk):
                            talk += adjustmentedTalk[i]
                            i = i + 1
                            
                        d_today = datetime.date.today()
                        
                        wks.update_cell(writeInAmount + 2, 1, selectedThread[0][4])
                        wks.update_cell(writeInAmount + 2, 2, selectedThread[0][0])
                        wks.update_cell(writeInAmount + 2, 3, talk)
                        wks.update_cell(writeInAmount + 2, 4, d_today.strftime('%Y-%m-%d'))
                        st.experimental_rerun()
                    elif talk == "":
                        st.error("未入力です")

            if st.button('戻る',key=1):
                pageFlag[0] = 0
                writingList.clear()
                password.clear()
                st.experimental_rerun()

            wks = gc.open('pyStreamlitBulletinboard').worksheet('シート2')
            allWriteIn = wks.get_all_values()
            print(allWriteIn)
            print(allWriteIn[1][0])
            writeInAmount = len(allWriteIn) - 1
            print(writeInAmount)

            selectedAllWriting = []
            selectedAllWritingDate = []
            for i in range(1,len(allWriteIn)):
                if int(allWriteIn[i][0]) == int(selectedThread[0][4]):
                    selectedAllWriting.append(allWriteIn[i][2])
                    selectedAllWritingDate.append(allWriteIn[i][3])
            print(selectedAllWriting)
            print(selectedAllWritingDate)

            html_style2 = """
            <style>
            #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div.css-1l3xw0p.e1tzin5v3 > div > div:nth-child(1) > div:nth-child(1) > div > div > button
            {
                margin-left: 85%;
            }

            #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div.css-1l3xw0p.e1tzin5v3 > div > div:nth-child(2) > div:nth-child(1) > div > div > button
            {
                margin-left: 25%;
            }

            #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div:nth-child(10) > div > button
            {
                margin-left: 91%;
            }

            #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div.css-1mg5w7t.epcbefy1 > div:nth-child(1) > div:nth-child(1) > div > div > button
            {
                margin-left: 83%;
            }

            #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.eknhn3m1 > div > div:nth-child(1) > div:nth-child(13) > div > button
            {
                margin-left: 91%;
            }
            </slyle>
            """

            st.markdown(html_style2,unsafe_allow_html=True)
                
            with st.form('inThread'):
                if st.form_submit_button("再読み込み"):
                    time.sleep(3)
                    st.experimental_rerun()

                for i in reversed(range(0,len(selectedAllWriting),1)):
                    stc.html("<hr>",None,9)

                    col_date, col_info= st.columns([1,8])

                    with col_date:
                        st.write("<span style='font-size: 13px;'>%s</span>"%selectedAllWritingDate[i],unsafe_allow_html=True)
                    with col_info:
                        st.info(selectedAllWriting[i])

        if st.button('戻る',key=2):
            pageFlag[0] = 0
            writingList.clear()
            password.clear()
            st.experimental_rerun()

if __name__ == '__main__':
    	main()
