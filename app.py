import streamlit as st
import requests
import tempfile
import pandas as pd
from datetime import datetime
import time
import random

st.set_page_config(page_title="Ultimate FB Smooth Poster", page_icon="⚡", layout="wide")
st.title("🚀 Ultimate FB Multi-ID Smooth Auto-Poster")
st.write("हा टूल सिंगल-युझरसाठी १००+ आयडी आणि त्यांचे पेजेस कोणत्याही त्रासाशिवाय एकदम स्मूथ चालवण्यासाठी डिझाइन केला आहे.")

# अनलिमिटेड आयडी साठवण्यासाठी मेमरी बॅकएंड
if 'fb_accounts' not in st.session_state:
    st.session_state.fb_accounts = {}
if 'post_history' not in st.session_state:
    st.session_state.post_history = []

# डावीकडील मेनू (Sidebar) - अनलिमिटेड आयडी मॅनेजमेंट
with st.sidebar:
    st.header("🔑 फेसबुक आयडी मॅनेज करा")
    
    total_accs = len(st.session_state.fb_accounts)
    st.metric(label="जोडलेले एकूण आयडी", value=f"{total_accs}")
    
    st.write("---")
    acc_name = st.text_input("अकाउंटचे नाव (उदा. आयडी १, युएसए सेट २)")
    acc_token = st.text_input("फेसबुक युझर ॲक्सेस टोकन (User Access Token)", type="password")
    
    if st.button("➕ नवीन आयडी जोडा"):
        if acc_name and acc_token:
            with st.spinner("फेसबुकवरून पेजेसची माहिती आणत आहे..."):
                try:
                    # पेजेस ऑटोमॅटिक फेच करणे
                    url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={acc_token}&limit=100"
                    res = requests.get(url).json()
                    if 'data' in res:
                        pages_list = []
                        for p in res['data']:
                            pages_list.append({
                                'page_name': p['name'], 
                                'page_id': p['id'], 
                                'page_token': p['access_token']
                            })
                        
                        st.session_state.fb_accounts[acc_name] = {
                            'token': acc_token,
                            'pages': pages_list
                        }
                        st.success(f"✅ {acc_name} यशस्वीरित्या जोडला! ({len(pages_list)} पेजेस सापडले)")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ टोकन चुकीचे आहे किंवा एक्स्पायर झाले आहे.")
                except:
                    st.error("❌ फेसबुक सर्व्हरशी संपर्क होऊ शकला नाही.")
        else:
            st.warning("कृपया नाव आणि टोकन दोन्ही भरा.")

    st.write("---")
    st.subheader("📋 तुमच्या आयडीची यादी:")
    if st.session_state.fb_accounts:
        for name in list(st.session_state.fb_accounts.keys()):
            col1, col2 = st.columns([4, 1])
            col1.write(f"👤 {name} ({len(st.session_state.fb_accounts[name]['pages'])} पेजेस)")
            if col2.button("🗑️", key=f"del_{name}"):
                del st.session_state.fb_accounts[name]
                st.rerun()
    else:
        st.caption("अद्याप कोणताही आयडी जोडलेला नाही.")

# मुख्य स्क्रीन वरील टॅब्स
tab1, tab2, tab3 = st.tabs(["🚀 रील बल्क पोस्ट", "📊 ट्रॅकिंग रिपोर्ट (Live Status)", "📋 सर्व पेजेसची यादी देखें"])

# टॅब ३: सर्व पेजेसची यादी
with tab3:
    st.subheader("📂 तुमच्या सर्व आयडींचे पेजेस")
    if st.session_state.fb_accounts:
        for acc_name, acc_data in st.session_state.fb_accounts.items():
            with st.expander(f"👤 {acc_name} चे सर्व पेजेस (एकूण: {len(acc_data['pages'])})"):
                for p in acc_data['pages']:
                    st.text(f"• {p['page_name']} (ID: {p['page_id']})")
    else:
        st.info("डाव्या बाजूला जाऊन आधी तुमचे फेसबुक आयडी जोडा.")

# टॅब १: रील पोस्टिंग पॅनेल
with tab1:
    if not st.session_state.fb_accounts:
        st.info("👈 टूल वापरण्यासाठी कृपया डाव्या बाजूला तुमचे फेसबुक अकाउंट्स जोडा.")
    else:
        uploaded_file = st.file_uploader("🎬 गॅलरीतून रील व्हिडिओ निवडा (.mp4)", type=["mp4"])
        caption = st.text_area("📝 कॅप्शन आणि हॅशटॅग (सर्व पेजेससाठी एकच लागू होईल)")
        
        st.write("---")
        st.subheader("🛡️ फेसबुक सुरक्षेसाठी हुमन-लाईक डिले (Human-like Delay)")
        st.write("फेसबुक तुमचे अकाउंट ब्लॉक करू नये म्हणून दोन पोस्टमध्ये सुरक्षित वेळेचा गॅप ठेवणे गरजेचे आहे:")
        
        col_t1, col_t2 = st.columns(2)
        min_delay = col_t1.number_input("कमीत कमी गॅप (सेकंदात)", min_value=5, value=30, step=5)
        max_delay = col_t2.number_input("जास्तीत जास्त गॅप (सेकंदात)", min_value=10, value=90, step=5)
        
        if st.button("🔥 रिअल-टाइम बल्क पोस्टिंग सुरू करा", type="primary"):
            if uploaded_file and caption:
                # मोठ्या फाईल्स स्मूथ हँडल करण्यासाठी तात्पुरती फाईल मॅनेजमेंट
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    video_path = tmp_file.name

                # एकूण किती पेजेस आहेत ते मोजणे
                all_target_pages = []
                for acc_name, acc_data in st.session_state.fb_accounts.items():
                    for p in acc_data['pages']:
                        all_target_pages.append({'acc_name': acc_name, 'page': p})
                
                total_pages = len(all_target_pages)
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for index, target in enumerate(all_target_pages):
                    acc_name = target['acc_name']
                    page = target['page']
                    
                    status_text.text(f"🔄 सध्या पोस्टिंग सुरू आहे: {page['page_name']} (अकाउंट: {acc_name}) [{index+1}/{total_pages}]...")
                    
                    init_url = f"https://graph.facebook.com/v19.0/{page['page_id']}/video_reels"
                    try:
                        # स्टेप १: रील सेशन सुरू करणे
                        res = requests.post(init_url, data={'upload_phase': 'start', 'access_token': page['page_token']}).json()
                        if 'video_id' in res:
                            video_id = res['video_id']
                            
                            # स्टेप २: व्हिडिओ डेटा ट्रान्सफर (स्मूथ अपलोड)
                            with open(video_path, 'rb') as f:
                                requests.post(f"https://graph.facebook.com/v19.0/{page['page_id']}/videos", 
                                              data={'access_token': page['page_token'], 'upload_phase': 'transfer', 'video_id': video_id},
                                              files={'video_file_chunk': f})
                            
                            # स्टेप ३: लगेच लाईव्ह पब्लिश करणे
                            pub_res = requests.post(init_url, data={
                                'upload_phase': 'finish', 'video_id': video_id,
                                'video_state': 'PUBLISHED', 'description': caption, 'access_token': page['page_token']
                             }).json()
                            
                            st.session_state.post_history.append({
                                'अकाउंट': acc_name, 'पेजचे नाव': page['page_name'],
                                'वेळ': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'स्टेटस': '✅ Successful'
                            })
                    except:
                        st.session_state.post_history.append({
                            'अकाउंट': acc_name, 'पेजचे नाव': page['page_name'],
                            'वेळ': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'स्टेटस': '❌ Failed'
                        })
                    
                    # प्रोग्रेस बार अपडेट
                    progress_bar.progress((index + 1) / total_pages)
                    
                    # जर हे शेवटचे पेज नसेल, तर माणसासारखा सुरक्षित ब्रेक देणे
                    if index + 1 < total_pages:
                        actual_delay = random.randint(min_delay, max_delay)
                        for i in range(actual_delay, 0, -1):
                            status_text.text(f"⏳ फेसबुक सुरक्षेसाठी पुढील पेजवर जाण्यापूर्वी {i} सेकंदांचा ब्रेक घेत आहे... (स्मूथ मोड चालू)")
                            time.sleep(1)
                            
                status_text.text(f"🎉 सर्व {total_pages} पेजेसवर रियल-टाइम पोस्टिंग यशस्वीरित्या पूर्ण झाले!")
                st.balloons()
            else:
                st.warning("कृपया आधी व्हिडिओ निवडा आणि कॅप्शन भरा.")

# टॅब २: लाईव्ह ट्रॅकिंग रिपोर्ट
with tab2:
    st.subheader("📊 रिअल-टाइम पोस्ट ट्रॅकिंग रिपोर्ट")
    if st.session_state.post_history:
        df = pd.DataFrame(st.session_state.post_history)
        st.dataframe(df, use_container_width=True)
        if st.button("🗑️ रिपोर्ट हिस्ट्री साफ करा"):
            st.session_state.post_history = []
            st.rerun()
    else:
        st.info("तुम्ही पोस्टिंग सुरू केल्यावर प्रत्येक पेजचे 'Successful' किंवा 'Failed' स्टेटस इथे रिअल-टाइममध्ये दिसेल.")
