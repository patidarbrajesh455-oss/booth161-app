import streamlit as st
import pandas as pd

# पेज की सेटिंग
st.set_page_config(page_title="बूथ 161 - वोटर मतदान ट्रैकर", layout="wide")

st.title("🗳️ सुसनेर विधानसभा - बूथ 161 (लटूरी गेहलोत)")
st.subheader("मतदान प्रबंधन डैशबोर्ड (Voter Turnout Tracker)")

# 1. वोटर लिस्ट का डेटा (डेटाबेस)
if 'voters_data' not in st.session_state:
    st.session_state['voters_data'] = [
        {"id": 1, "name": "राजाराम", "guardian": "कंवरलाल", "house_no": "1", "status": "Pending"},
        {"id": 2, "name": "लीलाबाई", "guardian": "राजाराम", "house_no": "1", "status": "Pending"},
        {"id": 3, "name": "कोशल्याबाई", "guardian": "कालूराम", "house_no": "1", "status": "Pending"},
        {"id": 4, "name": "कैलाशचन्द", "guardian": "कंवरलाल", "house_no": "1", "status": "Pending"},
        {"id": 5, "name": "विष्णुप्रसाद", "guardian": "कंवरलाल", "house_no": "1", "status": "Pending"},
        {"id": 6, "name": "सुगनबाई", "guardian": "कैलाशचन्द", "house_no": "1", "status": "Pending"},
        {"id": 7, "name": "धापुबाई", "guardian": "विष्णुप्रसाद", "house_no": "1", "status": "Pending"},
        {"id": 8, "name": "संजय कुमार", "guardian": "कालूराम", "house_no": "1", "status": "Pending"},
        {"id": 9, "name": "सतीश कुमार पाटीदार", "guardian": "कैलाशचन्द", "house_no": "1", "status": "Pending"},
        {"id": 10, "name": "अनुसुईया पाटीदार", "guardian": "संजय कुमार", "house_no": "01", "status": "Pending"}
    ]

df = pd.DataFrame(st.session_state['voters_data'])

# 2. ऊपर डैशबोर्ड का स्टेट्स (कुल वोटर, वोट डल चुके, बाकी हैं)
total_voters = len(df)
voted_count = len(df[df['status'] == 'Voted'])
pending_count = len(df[df['status'] == 'Pending'])

col1, col2, col3 = st.columns(3)
col1.metric("कुल मतदाता (Total)", total_voters)
col2.metric("वोट डाल चुके (Voted)", voted_count, delta_color="normal")
col3.metric("बाकी हैं (Pending)", pending_count, delta_color="inverse")

st.markdown("---")

# 3. सर्च करने का विकल्प
search_query = st.text_input("🔍 मतदाता का नाम या घर नंबर खोजें:", "")

if search_query:
    filtered_df = df[df['name'].str.contains(search_query, na=False) | df['house_no'].str.contains(search_query, na=False)]
else:
    filtered_df = df

st.markdown("### 📋 मतदाताओं की सूची और मतदान स्थिति")

# 4. टेबल फॉर्मेट में लिस्ट दिखाना और हर वोटर के आगे हरे/लाल बटन देना
for index, row in filtered_df.iterrows():
    col_info, col_btn1, col_btn2 = st.columns([4, 1, 1])
    
    with col_info:
        status_icon = "🟢" if row['status'] == "Voted" else "🔴"
        st.write(f"{status_icon} **{row['name']}** (पिता/पति: {row['guardian']} | घर नं: {row['house_no']}) — स्थिति: *{row['status']}*")
    
    # हरा बटन (मतदान हो गया)
    with col_btn1:
        if row['status'] == "Pending":
            if st.button("✅ वोट डल गया", key=f"voted_{row['id']}"):
                st.session_state['voters_data'][index]['status'] = "Voted"
                st.rerun()
        else:
            st.success("डाल दिया")

    # लाल/रीसेट बटन
    with col_btn2:
        if row['status'] == "Voted":
            if st.button("🔄 रीसेट", key=f"reset_{row['id']}"):
                st.session_state['voters_data'][index]['status'] = "Pending"
                st.rerun()

st.markdown("---")

# 5. अलग से "वोट डाल चुके लोगों की लिस्ट" देखने का सेक्शन
with st.expander("📥 जिन मतदाताओं का मतदान हो गया है उनकी लिस्ट देखें"):
    voted_df = df[df['status'] == 'Voted']
    if not voted_df.empty:
        st.table(voted_df[['name', 'guardian', 'house_no']])
    else:
        st.info("अभी तक किसी भी मतदाता का डेटा 'Voted' के रूप में अपडेट नहीं किया गया है।")