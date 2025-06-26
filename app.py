import streamlit as st
import pandas as pd
from email_classifier import classify_emails
from whatsapp_classifier import classify_whatsapp
from utils.gmail_api import fetch_recent_emails
from utils.user_storage import save_user, load_users

st.set_page_config(page_title="AutoClean Inbox", layout="wide")
st.title("📬 AutoClean Inbox — Spam Detector for Gmail + WhatsApp")

tab1, tab2, tab3 = st.tabs(["📩 Gmail Spam Detection", "💬 WhatsApp Spam Detection", "👤 Manage Users"])

# ----------------------- Gmail Spam Detection -----------------------
with tab1:
    st.subheader("📬 Gmail Spam Detection")

    users = load_users()
    if not users:
        st.warning("⚠️ No Gmail users saved yet. Add some in the 'Manage Users' tab.")
    else:
        for idx, user in enumerate(users):
            with st.expander(f"{idx+1}. {user['email']}"):
                if st.button(f"🚀 Fetch & Classify: {user['email']}", key=f"classify_{idx}"):
                    try:
                        st.info(f"Connecting to {user['email']}...")
                        messages = fetch_recent_emails()
                        predictions = classify_emails(messages)

                        if not messages:
                            st.warning("📭 No emails fetched.")
                        else:
                            df = pd.DataFrame({
                                "Message": messages,
                                "Prediction": predictions
                            })

                            spam_df = df[df["Prediction"] == "spam"]
                            ham_df = df[df["Prediction"] == "ham"]

                            st.success(f"✅ Processed {len(df)} emails — 🧹 {len(spam_df)} spam, ✅ {len(ham_df)} ham")

                            st.subheader("🧹 Detected Spam Messages")
                            if not spam_df.empty:
                                st.dataframe(spam_df)
                                st.download_button(
                                    "📥 Download Spam Only",
                                    spam_df.to_csv(index=False),
                                    file_name=f"{user['email'].replace('@', '_')}_spam_only.csv"
                                )
                            else:
                                st.info("🎉 No spam messages detected.")

                            st.subheader("📋 All Emails")
                            st.dataframe(df)
                            st.download_button(
                                "⬇ Download All Emails",
                                df.to_csv(index=False),
                                file_name=f"{user['email'].replace('@', '_')}_all.csv"
                            )
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

# ----------------------- WhatsApp Spam Detection -----------------------
with tab2:
    st.subheader("💬 WhatsApp Chat Classifier")

    uploaded_file = st.file_uploader("📤 Upload WhatsApp Chat (.txt)", type=["txt"])
    if uploaded_file:
        try:
            st.info("🔄 Processing WhatsApp messages...")
            text = uploaded_file.read().decode("utf-8")
            messages, predictions = classify_whatsapp(text)

            df = pd.DataFrame({
                "Message": messages,
                "Prediction": predictions
            })

            spam_df = df[df["Prediction"] == "spam"]
            st.success(f"✅ Processed {len(df)} messages — 🧹 {len(spam_df)} spam detected")

            st.subheader("📋 All WhatsApp Messages")
            st.dataframe(df)

            format = st.selectbox("📂 Download Format", ["CSV", "JSON"], key="whatsapp_dl")
            if format == "CSV":
                st.download_button("📥 Download CSV", df.to_csv(index=False), "cleaned_whatsapp.csv")
            else:
                st.download_button("📥 Download JSON", df.to_json(orient="records"), "cleaned_whatsapp.json")

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ----------------------- User Management Tab -----------------------
with tab3:
    st.subheader("👤 Add Gmail User")
    email = st.text_input("📧 Gmail Address")
    password = st.text_input("🔑 Gmail App Password", type="password")

    if st.button("➕ Save User"):
        if email and password:
            try:
                save_user(email, password)
                st.success("✅ User saved successfully!")
            except Exception as e:
                st.error(f"❌ Failed to save user: {e}")
        else:
            st.warning("Please enter both Gmail and app password.")
