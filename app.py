import streamlit as st
import requests
import json

SUPABASE_URL = "https://reiayveqbmlvnsfkxcal.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJlaWF5dmVxYm1sdm5zZmt4Y2FsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE4ODc0MjYsImV4cCI6MjA3NzQ2MzQyNn0.HYRXvPcX5Ttn18wuYpfSLoVBUoM6-2y1V1w3iBuUhVw"

def search_gayo_knowledge(query):
    """
    Search Gayo language knowledge base with detailed debugging
    """
    if not query or len(query.strip()) < 2:
        return "❌ Masukkan minimal 2 karakter untuk pencarian."
    
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        # Enhanced search with better query
        url = f"{SUPABASE_URL}/rest/v1/gayo_knowledge_base"
        params = {
            "gayo_word": f"ilike.%{query}%",
            "select": "*,cultural_context,word_class,indonesian_meaning"
        }
        
        st.info(f"🔍 Mencari: '{query}' di Supabase...")
        
        response = requests.get(url, headers=headers, params=params)
        
        # Debug information
        st.write(f"📡 Status Code: {response.status_code}")
        st.write(f"🔗 URL: {url}")
        
        if response.status_code == 200:
            results = response.json()
            st.write(f"📊 Jumlah hasil: {len(results)}")
            
            if results:
                output = f"## 🔍 Ditemukan {len(results)} hasil untuk '{query}'\n\n"
                
                for i, item in enumerate(results, 1):
                    gayo_word = item.get('gayo_word', 'N/A')
                    indonesian_meaning = item.get('indonesian_meaning', 'Tidak tersedia')
                    word_class = item.get('word_class', 'Tidak tersedia')
                    cultural_context = item.get('cultural_context', '')
                    
                    output += f"### {i}. **{gayo_word}**\n"
                    output += f"**Makna Indonesia:** {indonesian_meaning}\n"
                    output += f"**Kelas Kata:** {word_class}\n"
                    
                    if cultural_context:
                        output += f"**🏛️ Konteks Budaya:** {cultural_context}\n"
                    
                    output += "---\n\n"
                
                cultural_count = sum(1 for item in results if item.get('cultural_context'))
                output += f"**📊 Statistik:** {cultural_count} dari {len(results)} hasil memiliki konteks budaya\n"
                
                return output
            else:
                # Test dengan query yang lebih simple
                st.warning("Tidak ada hasil. Testing dengan query alternatif...")
                
                # Coba query alternatif
                test_params = {
                    "select": "*",
                    "limit": 5
                }
                test_response = requests.get(url, headers=headers, params=test_params)
                
                if test_response.status_code == 200:
                    test_data = test_response.json()
                    if test_data:
                        return f"✅ Koneksi Supabase berhasil! Database memiliki {len(test_data)} entri. Coba kata kunci lain."
                    else:
                        return "❌ Database kosong atau tidak ada data."
                else:
                    return f"❌ Error test connection: {test_response.status_code}"
                    
        else:
            return f"❌ Error API: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"❌ Exception: {str(e)}"

def test_supabase_connection():
    """Test koneksi ke Supabase"""
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        url = f"{SUPABASE_URL}/rest/v1/gayo_knowledge_base"
        params = {"limit": 1}
        
        response = requests.get(url, headers=headers, params=params)
        return response.status_code, response.json() if response.status_code == 200 else None
    except Exception as e:
        return None, str(e)

# Streamlit UI
st.set_page_config(
    page_title="🤖 AI Assistant Bahasa Gayo - Bener Meriah",
    page_icon="🏔️",
    layout="wide"
)

st.title("🤖 AI Assistant Bahasa Gayo - Bener Meriah")
st.markdown("### 🏔️ Pelestarian Budaya dan Bahasa Gayo melalui Teknologi AI")

# Test connection first
st.subheader("🔧 Connection Test")
if st.button("Test Koneksi Supabase"):
    status, data = test_supabase_connection()
    if status == 200:
        st.success(f"✅ Koneksi Supabase BERHASIL! Status: {status}")
        if data:
            st.info(f"📊 Sample data: {json.dumps(data[0], indent=2)}")
    else:
        st.error(f"❌ Koneksi Supabase GAGAL! Status: {status}, Error: {data}")

st.markdown("---")

# Main Search
st.subheader("🔍 Cari Pengetahuan Gayo")
query = st.text_input(
    "Masukkan kata dalam Bahasa Indonesia:",
    placeholder="Contoh: makan, rumah, adat...",
    key="search_input"
)

if st.button("🚀 Cari", type="primary") or query:
    if query and len(query.strip()) >= 2:
        with st.spinner("Mencari dalam basis pengetahuan..."):
            result = search_gayo_knowledge(query)
            st.markdown(result)
    elif query:
        st.warning("Masukkan minimal 2 karakter")

# Quick tests
st.markdown("---")
st.subheader("🎯 Quick Tests")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🍚 Test: makan"):
        with st.spinner("Testing..."):
            result = search_gayo_knowledge("makan")
            st.markdown(result)

with col2:
    if st.button("🏠 Test: rumah"):
        with st.spinner("Testing..."):
            result = search_gayo_knowledge("rumah")
            st.markdown(result)

with col3:
    if st.button("📚 Test: a"):
        with st.spinner("Testing..."):
            result = search_gayo_knowledge("a")
            st.markdown(result)

with col4:
    if st.button("🔍 Test: semua"):
        with st.spinner("Testing..."):
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            }
            url = f"{SUPABASE_URL}/rest/v1/gayo_knowledge_base"
            params = {"limit": 10}
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ Total entries: {len(data)}")
                for item in data[:3]:  # Show first 3
                    st.write(f"- {item.get('gayo_word', 'N/A')}: {item.get('indonesian_meaning', 'N/A')}")
            else:
                st.error(f"❌ Error: {response.status_code}")
