import streamlit as st
import requests
import json

SUPABASE_URL = "https://reiayveqbmlvnsfkxcal.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJlaWF5dmVxYm1sdm5zZmt4Y2FsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE4ODc0MjYsImV4cCI6MjA3NzQ2MzQyNn0.HYRXvPcX5Ttn18wuYpfSLoVBUoM6-2y1V1w3iBuUhVw"

def search_gayo_knowledge(query):
    """
    Search Gayo language knowledge base with correct column names
    """
    if not query or len(query.strip()) < 2:
        return "❌ Masukkan minimal 2 karakter untuk pencarian."
    
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        # CORRECT QUERY - menggunakan kolom yang sesuai dengan struktur database
        url = f"{SUPABASE_URL}/rest/v1/gayo_knowledge_base"
        
        # Query yang benar berdasarkan struktur data sample
        params = {
            "select": "id,text,metadata",
            "or": f"(text.ilike.%{query}%,metadata->>gayo_word.ilike.%{query}%,metadata->>indonesian_meaning.ilike.%{query}%)",
            "limit": 8
        }
        
        st.info(f"🔍 Mencari: '{query}'...")
        
        response = requests.get(url, headers=headers, params=params)
        
        st.write(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            st.write(f"📊 Hasil ditemukan: {len(results)}")
            
            if results:
                output = f"## 🔍 Ditemukan {len(results)} hasil untuk '{query}'\n\n"
                
                for i, item in enumerate(results, 1):
                    # Extract data dari struktur yang benar
                    text = item.get('text', '')
                    metadata = item.get('metadata', {})
                    
                    gayo_word = metadata.get('gayo_word', 'N/A')
                    indonesian_meaning = metadata.get('indonesian_meaning', 'Tidak tersedia')
                    word_class = metadata.get('pos_tag', 'Tidak tersedia')
                    cultural_context = metadata.get('cultural_context', False)
                    
                    # Jika tidak ada di metadata, coba extract dari text
                    if gayo_word == 'N/A' and 'KATA GAYO:' in text:
                        try:
                            gayo_word = text.split('KATA GAYO:')[1].split('.')[0].strip()
                        except:
                            gayo_word = 'N/A'
                    
                    output += f"### {i}. **{gayo_word}**\n"
                    output += f"**Makna Indonesia:** {indonesian_meaning}\n"
                    output += f"**Kelas Kata:** {word_class}\n"
                    
                    if cultural_context:
                        output += f"**🏛️ Memiliki konteks budaya**\n"
                    
                    output += "---\n\n"
                
                cultural_count = sum(1 for item in results if item.get('metadata', {}).get('cultural_context'))
                output += f"**📊 Statistik:** {cultural_count} dari {len(results)} hasil memiliki konteks budaya\n"
                
                return output
            else:
                return f"❌ Tidak ditemukan hasil untuk '{query}'. Coba kata kunci lain."
        else:
            return f"❌ Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"❌ Exception: {str(e)}"

def get_database_structure():
    """Get database structure untuk debugging"""
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        url = f"{SUPABASE_URL}/rest/v1/gayo_knowledge_base"
        params = {"limit": 1, "select": "*"}
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]  # Return first item structure
        return None
    except Exception as e:
        return str(e)

# Streamlit UI
st.set_page_config(
    page_title="AI Assistant Bahasa Gayo",
    page_icon="🏔️",
    layout="wide"
)

st.title("AI Assistant Bahasa Gayo")
st.markdown("### pendukung Neniwer untuk memahami bahasa Gayo")

# Database Structure Debug
st.subheader("🔧 Database Structure")
if st.button("Lihat Struktur Database"):
    structure = get_database_structure()
    if structure:
        st.success("✅ Struktur database ditemukan:")
        st.json(structure)
    else:
        st.error("❌ Gagal mendapatkan struktur database")

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

# Quick tests dengan query yang work
st.markdown("---")
st.subheader("🎯 Test dengan Kata yang Diketahui")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🍚 Test: Titok"):
        with st.spinner("Testing..."):
            result = search_gayo_knowledge("Titok")
            st.markdown(result)

with col2:
    if st.button("🔧 Test: Alat"):
        with st.spinner("Testing..."):
            result = search_gayo_knowledge("Alat")
            st.markdown(result)

with col3:
    if st.button("📖 Test: sirih"):
        with st.spinner("Testing..."):
            result = search_gayo_knowledge("sirih")
            st.markdown(result)

# Show sample data
st.markdown("---")
st.subheader("📋 Sample Data dari Database")
if st.button("Tampilkan Sample Data"):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    url = f"{SUPABASE_URL}/rest/v1/gayo_knowledge_base"
    params = {"limit": 5}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        st.success(f"✅ Menampilkan {len(data)} sample entries:")
        for i, item in enumerate(data, 1):
            with st.expander(f"Entry {i}: {item.get('metadata', {}).get('gayo_word', 'N/A')}"):
                st.json(item)
    else:
        st.error(f"❌ Error: {response.status_code}")
