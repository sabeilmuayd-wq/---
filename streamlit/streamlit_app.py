import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="بودا بودا السودانيين",
    page_icon="🛵",
    layout="wide"
)

# ====== CSS للعربية RTL ======
st.markdown("""
<style>
    body, .stApp { direction: rtl; text-align: right; }
    .stTextInput input, .stSelectbox select { direction: rtl; }
    h1, h2, h3 { text-align: right; }
</style>
""", unsafe_allow_html=True)

st.title("🛵 بودا بودا السودانيين - كيرياندونقو")
st.caption("توصيل آمن • سواقين سودانيين • أسعار واضحة")

# ====== تخزين مؤقت ======
if 'rides' not in st.session_state:
    st.session_state.rides = []

if 'drivers' not in st.session_state:
    st.session_state.drivers = [
        {"الاسم": "أحمد محمد", "المنطقة": "Zone 1", "الهاتف": "+256700111111", "متاح": "✅"},
        {"الاسم": "محمد علي", "المنطقة": "Zone 2", "الهاتف": "+256700222222", "متاح": "✅"},
        {"الاسم": "عبدالله يوسف", "المنطقة": "Zone 3", "الهاتف": "+256700333333", "متاح": "⏳"},
        {"الاسم": "يوسف إبراهيم", "المنطقة": "كيرياندونقو", "الهاتف": "+256700444444", "متاح": "✅"},
    ]

# ====== التبويبات ======
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 طلب رحلة",
    "🏍️ السائقين",
    "📊 السجل",
    "➕ إضافة سائق"
])

# ====== تبويب 1: طلب رحلة ======
with tab1:
    st.header("اطلب بودا الآن")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("اسمك الكامل", key="r_name")
        phone = st.text_input("رقم هاتفك", key="r_phone")
        area = st.selectbox("منطقتك", [
            "كيرياندونقو - Zone 1",
            "كيرياندونقو - Zone 2",
            "كيرياندونقو - Zone 3",
            "كيرياندونقو - وسط",
            "كامبالا"
        ], key="r_area")
    
    with col2:
        destination = st.text_input("إلى أين؟", key="r_dest")
        notes = st.text_area("ملاحظات (اختياري)", key="r_notes")
    
    if st.button("🛵 اطلب الآن", use_container_width=True, type="primary"):
        if name and phone and destination:
            new_ride = {
                "الاسم": name,
                "الهاتف": phone,
                "من": area,
                "إلى": destination,
                "ملاحظات": notes,
                "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "الحالة": "قيد الانتظار"
            }
            st.session_state.rides.append(new_ride)
            st.success(f"✅ تم الطلب يا {name}! سيتصل بك سائق قريباً")
            st.balloons()
        else:
            st.warning("⚠️ أكمل الحقول المطلوبة: الاسم، الهاتف، الوجهة")

# ====== تبويب 2: السائقين ======
with tab2:
    st.header("السائقين المتاحين")
    
    if st.session_state.drivers:
        df = pd.DataFrame(st.session_state.drivers)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.subheader("اتصل مباشرة")
        for d in st.session_state.drivers:
            if d["متاح"] == "✅":
                st.markdown(f"**{d['الاسم']}** — {d['المنطقة']} — [{d['الهاتف']}](tel:{d['الهاتف']})")
    else:
        st.info("لا يوجد سائقون بعد")

# ====== تبويب 3: السجل ======
with tab3:
    st.header("سجل الرحلات")
    
    if st.session_state.rides:
        col1, col2, col3 = st.columns(3)
        col1.metric("عدد الرحلات", len(st.session_state.rides))
        col2.metric("العمولة المتوقعة", f"{len(st.session_state.rides) * 500} UGX")
        col3.metric("السائقين النشطين", len([d for d in st.session_state.drivers if d['متاح'] == '✅']))
        
        st.divider()
        df = pd.DataFrame(st.session_state.rides)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        if st.button("🗑️ حذف كل السجل"):
            st.session_state.rides = []
            st.rerun()
    else:
        st.info("لا توجد رحلات بعد")

# ====== تبويب 4: إضافة سائق ======
with tab4:
    st.header("إضافة سائق جديد")
    
    with st.form("add_driver"):
        d_name = st.text_input("اسم السائق")
        d_area = st.selectbox("منطقته", [
            "Zone 1", "Zone 2", "Zone 3", "كيرياندونقو - وسط"
        ])
        d_phone = st.text_input("رقم هاتفه")
        d_available = st.selectbox("متاح؟", ["✅", "⏳"])
        
        submitted = st.form_submit_button("➕ إضافة السائق", use_container_width=True)
        
        if submitted:
            if d_name and d_phone:
                st.session_state.drivers.append({
                    "الاسم": d_name,
                    "المنطقة": d_area,
                    "الهاتف": d_phone,
                    "متاح": d_available
                })
                st.success(f"✅ تم إضافة {d_name}")
                st.rerun()
            else:
                st.warning("أكمل الاسم والهاتف")

# ====== الفوتر ======
st.divider()
st.caption("🛵 بودا بودا السودانيين | كيرياندونقو، أوغندا | للتواصل: +256 XXX XXX XXX")
