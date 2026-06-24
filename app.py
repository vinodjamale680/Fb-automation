import streamlit as st
import requests

st.set_page_config(page_title="FB Multi-Page Poster", page_icon="🚀")
st.title("📱 FB Multi-Page Auto-Poster")

# युझर कितीही पेजेस जोडू शकतो (डेटाबेस सोय)
if 'pages' not in st.session_state:
    st.session_state.pages = []

# टॅब सिस्टीम
tab1, tab2 = st.tabs(["🎬 Reels अपलोड करा", "⚙️ पेजेस मॅनेज करा"])

with tab2:
    st.subheader("नवीन फेसबुक पेज जोडा")
    p_name = st.text_input("पेजचे नाव (उदा. Page 1)")
    p_id = st.text_input("Page ID")
    p_token = st.text_input("Page Access Token", type="password")
    
    if st.button("पेज सेव्ह करा"):
        if p_name and p_id and p_token:
            st.session_state.pages.append({"name": p_name, "id": p_id, "token": p_token})
            st.success(f"✅ {p_name} यशस्वीरित्या जोडले गेले!")
        else:
            st.warning("सर्व माहिती भरा!")
            
    st.write("---")
    st.write("📋 सध्या जोडलेले पेजेस:")
    for p in st.session_state.pages:
        st.text(f"• {p['name']} (ID: {p['id']})")

with tab1:
    st.subheader("सर्व पेजेसवर रील पाठवा")
    video_url = st.text_input("🎬 व्हिडिओची डायरेक्ट डाऊनलोड लिंक (URL) टाका")
    caption = st.text_area("📝 कॅप्शन आणि हॅशटॅग")
    
    if st.button("🚀 Publish to All Pages", type="primary"):
        if video_url and caption and st.session_state.pages:
            st.info("🔄 अपलोडिंग सुरू आहे...")
            success = 0
            for page in st.session_state.pages:
                init_url = f"https://graph.facebook.com/v19.0/{page['id']}/video_reels"
                try:
                    res = requests.post(init_url, data={'upload_phase': 'start', 'access_token': page['token']}).json()
                    if 'video_id' in res:
                        pub_url = f"https://graph.facebook.com/v19.0/{page['id']}/video_reels"
                        pub_res = requests.post(pub_url, data={
                            'upload_phase': 'finish', 'video_id': res['video_id'],
                            'video_state': 'PUBLISHED', 'description': caption, 'access_token': page['token']
                        }).json()
                        if 'id' in pub_res or pub_res.get('success'):
                            st.success(f"✅ {page['name']} वर रील गेली!")
                            success += 1
                except:
                    st.error(f"❌ {page['name']} वर एरर आला.")
            st.success(f"🎉 एकूण {success} पेजेसवर काम पूर्ण झाले!")
        else:
            st.warning("कृपया लिंक, कॅप्शन भरा आणि कमीत कमी १ पेज जोडा!")

