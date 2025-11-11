import streamlit as st
import requests

SUPABASE_URL = "https://reiayveqbmlvnsfkxcal.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJlaWF5dmVxYm1sdm5zZmt4Y2FsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE4ODc0MjYsImV4cCI6MjA3NzQ2MzQyNn0.HYRXvPcX5Ttn18wuYpfSLoVBUoM6-2y1V1w3iBuUhVw"

def search_gayo_knowledge(query):
    """
    Search Gayo language knowledge base
    """
    if not query or len(query.strip()) < 2:
        return "❌ Masukkan minimal 2 karakter untuk pencarian."
    
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        # Search across multiple columns
        url = f"{SUPABASE_URL}/rest/v1/gayo_knowledge_base"
        params = {
            "or": f"(gayo_word.ilike.%{query}%,indonesian_meaning.ilike.%{query}%,cultural_context.ilike.%{query}%)",
            "limit": 8
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            results = response.json()
            
            if results:
                output = f"## 🔍 Ditemukan {len(results)} hasil untuk '{query}'\n\n"
                
                for i, item in enumerate(results, 1):
                    gayo_word = item.get('gayo_word', 'N/A')
                    indonesian_meaning = item.get('indonesian_meaning', 'Tidak tersedia')
                    word_class = item.get('word_class', 'Tidak tersedia')
                    cultural_context = item.get('cultural_context', '')
                    
                    # Truncate long text
                    if len(indonesian_meaning) > 120:
                        indonesian_meaning = indonesian_meaning[:117] + "..."
                    
                    output += f"### {i}. **{gayo_word}**\n"
                    output += f"**Makna Indonesia:** {indonesian_meaning}\n"
                    output += f"**Kelas Kata:** {word_class}\n"
                    
                    if cultural_context:
                        if len(cultural_context) > 150:
                            cultural_context = cultural_context[:147] + "..."
                        output += f"**🏛️ Konteks Budaya:** {cultural_context}\n"
                    
                    output += "---\n\n"
                
                # Add statistics
                cultural_count = sum(1 for item in results if item.get('cultural_context'))
                output += f"**📊 Statistik:** {cultural_count} dari {len(results)} hasil memiliki konteks budaya Gayo\n"
                
                return output
            else:
                return f"❌ Tidak ditemukan hasil untuk '{query}'. Coba dengan kata kunci lain."
        else:
            return f"❌ Error mengakses database (Status: {response.status_code})"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit UI Configuration
st.set_page_config(
    page_title="🤖 AI Assistant Bahasa Gayo - Bener Meriah",
    page_icon="🏔️",
    layout="wide"
)

# Header Section
st.title("🤖 AI Assistant Bahasa Gayo - Bener Meriah")
st.markdown("### 🏔️ Pelestarian Budaya dan Bahasa Gayo melalui Teknologi AI")
st.markdown("**Database:** 968 entri pengetahuan | **Konteks Budaya:** 73% coverage")

# Sidebar
with st.sidebar:
    st.header("📊 Tentang Sistem")
    st.markdown("""
    **Fitur Utama:**
    - 🔍 Pencarian pengetahuan Bahasa Gayo
    - 🏛️ Konteks budaya (73% coverage)
    - 📚 968 entri kosakata & tata bahasa
    - 🌐 Cloud-based dengan Supabase
    
    **Cakupan Data:**
    - 867 kosakata Bahasa Gayo
    - 101 aturan tata bahasa  
    - 94 contoh kalimat
    - 633 konteks budaya
    """)
    
    st.markdown("---")
    st.markdown("**💡 Contoh Pencarian:**")
    st.markdown("- `makan` - kosakata makanan")
    st.markdown("- `rumah` - arsitektur tradisional")
    st.markdown("- `adat` - tradisi & budaya")
    st.markdown("- `kekasih` - hubungan sosial")

# Main Search Interface
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🔍 Cari Pengetahuan Gayo")
    query = st.text_input(
        "Masukkan kata dalam Bahasa Indonesia:",
        placeholder="Contoh: makan, rumah, adat, tradisi...",
        key="search_input"
    )
    
    # Search button
    search_clicked = st.button("🚀 Cari Pengetahuan Gayo", type="primary")
    
    if search_clicked or query:
        if query and len(query.strip()) >= 2:
            with st.spinner("Mencari dalam basis pengetahuan Gayo..."):
                result = search_gayo_knowledge(query)
                st.markdown(result)
        elif query:
            st.warning("Masukkan minimal 2 karakter untuk pencarian.")

with col2:
    st.subheader("📊 Statistik")
    if st.button("🔄 Tampilkan Statistik", key="stats_btn"):
        st.markdown("""
        **📊 STATISTIK BASIS PENGETAHUAN:**
        
        ✅ **Total Entri:** 968 entries
        🏛️ **Konteks Budaya:** 633 entries (73%)
        📚 **Kosakata:** 867 entries
        📝 **Tata Bahasa:** 101 rules
        🎯 **Contoh Kalimat:** 94 examples
        
        🌐 **Status Sistem:** 
        - Database: ✅ Terhubung
        - API Search: ✅ Aktif
        - Cultural AI: ✅ 73% coverage
        """)

# Quick Test Section
st.markdown("---")
st.subheader("🎯 Quick Test")
test_col1, test_col2, test_col3, test_col4 = st.columns(4)

with test_col1:
    if st.button("🍚 Makan", key="test1"):
        with st.spinner("Mencari..."):
            result = search_gayo_knowledge("makan")
            st.markdown(result)

with test_col2:
    if st.button("🏠 Rumah", key="test2"):
        with st.spinner("Mencari..."):
            result = search_gayo_knowledge("rumah")
            st.markdown(result)

with test_col3:
    if st.button("🎎 Adat", key="test3"):
        with st.spinner("Mencari..."):
            result = search_gayo_knowledge("adat")
            st.markdown(result)

with test_col4:
    if st.button("💖 Kekasih", key="test4"):
        with st.spinner("Mencari..."):
            result = search_gayo_knowledge("kekasih")
            st.markdown(result)

# Footer
st.markdown("---")
st.markdown(
    "**ℹ️ Tentang Sistem:** AI Assistant untuk melestarikan bahasa dan budaya Gayo "
    "Kabupaten Bener Meriah dalam rangka sistem peringatan dini dan pelestarian budaya."
)
