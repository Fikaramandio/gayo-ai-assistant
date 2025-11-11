import streamlit as st
import requests
import json

SUPABASE_URL = "https://reiayveqbmlvnsfkxcal.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJlaWF5dmVxYm1sdm5zZmt4Y2FsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE4ODc0MjYsImV4cCI6MjA3NzQ2MzQyNn0.HYRXvPcX5Ttn18wuYpfSLoVBUoM6-2y1V1w3iBuUhVw"

def search_gayo_knowledge(query):
    """
    Search Gayo language knowledge base - FINAL CORRECT VERSION
    """
    if not query or len(query.strip()) < 2:
        return "❌ Masukkan minimal 2 karakter untuk pencarian."
    
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        # CORRECT QUERY - Search in text field (contains all content)
        url = f"{SUPABASE_URL}/rest/v1/gayo_knowledge_base"
        
        # Search in the main text field which contains all the content
        params = {
            "select": "id,text,metadata",
            "text": f"ilike.%{query}%",
            "limit": 10
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            results = response.json()
            
            if results:
                output = f"## 🔍 Ditemukan {len(results)} hasil untuk '{query}'\n\n"
                
                for i, item in enumerate(results, 1):
                    text = item.get('text', '')
                    metadata = item.get('metadata', {})
                    
                    # Extract information from text
                    gayo_word = metadata.get('gayo_word', 'N/A')
                    indonesian_meaning = metadata.get('indonesian_meaning', '')
                    cultural_context = metadata.get('cultural_context', False)
                    
                    # If not in metadata, extract from text
                    if gayo_word == 'N/A' and 'KATA GAYO:' in text:
                        try:
                            gayo_word = text.split('KATA GAYO:')[1].split('.')[0].strip()
                        except:
                            gayo_word = 'N/A'
                    
                    # Extract Indonesian meaning from text if not in metadata
                    if not indonesian_meaning and 'Makna Indonesia:' in text:
                        try:
                            indonesian_meaning = text.split('Makna Indonesia:')[1].split('. Kelas Kata:')[0].strip()
                        except:
                            indonesian_meaning = 'Tidak tersedia'
                    
                    # Extract word class
                    word_class = 'Tidak tersedia'
                    if 'Kelas Kata:' in text:
                        try:
                            word_class = text.split('Kelas Kata:')[1].split('. Konteks Budaya:')[0].strip()
                        except:
                            pass
                    
                    # Format output
                    output += f"### {i}. **{gayo_word}**\n"
                    
                    if indonesian_meaning:
                        # Clean up the meaning
                        clean_meaning = indonesian_meaning.replace('**', '').strip()
                        if len(clean_meaning) > 150:
                            clean_meaning = clean_meaning[:147] + "..."
                        output += f"**Makna Indonesia:** {clean_meaning}\n"
                    
                    if word_class != 'Tidak tersedia':
                        output += f"**Kelas Kata:** {word_class}\n"
                    
                    if cultural_context:
                        output += f"**🏛️ Memiliki konteks budaya**\n"
                    elif 'Konteks Budaya: Ya' in text:
                        output += f"**🏛️ Memiliki konteks budaya**\n"
                    
                    output += "---\n\n"
                
                # Statistics
                cultural_count = 0
                for item in results:
                    if item.get('metadata', {}).get('cultural_context') or 'Konteks Budaya: Ya' in item.get('text', ''):
                        cultural_count += 1
                
                output += f"**📊 Statistik:** {cultural_count} dari {len(results)} hasil memiliki konteks budaya\n"
                
                return output
            else:
                return f"❌ Tidak ditemukan hasil untuk '{query}'. Coba kata kunci lain."
        else:
            return f"❌ Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"❌ Exception: {str(e)}"

def get_total_entries():
    """Get total number of entries"""
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        url = f"{SUPABASE_URL}/rest/v1/gayo_knowledge_base"
        params = {"select": "id", "limit": 1000}
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return len(response.json())
        return 0
    except:
        return 0

# Streamlit UI
st.set_page_config(
    page_title="🤖 AI Assistant Bahasa Gayo - Bener Meriah",
    page_icon="🏔️",
    layout="wide"
)

st.title("🤖 AI Assistant Bahasa Gayo - Bener Meriah")
st.markdown("### 🏔️ Pelestarian Budaya dan Bahasa Gayo melalui Teknologi AI")

# Stats
total_entries = get_total_entries()
st.markdown(f"**📊 Database:** {total_entries} entri pengetahuan | **🏛️ Konteks Budaya:** 73% coverage")

# Main Search
st.markdown("---")
st.subheader("🔍 Cari Pengetahuan Gayo")

col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "Masukkan kata dalam Bahasa Indonesia:",
        placeholder="Contoh: makan, rumah, adat, tradisi, alat...",
        key="search_input"
    )

with col2:
    st.markdown("")
    st.markdown("")
    search_clicked = st.button("🚀 Cari", type="primary", use_container_width=True)

if search_clicked or query:
    if query and len(query.strip()) >= 2:
        with st.spinner("🔍 Mencari dalam basis pengetahuan Gayo..."):
            result = search_gayo_knowledge(query)
            st.markdown(result)
    elif query:
        st.warning("Masukkan minimal 2 karakter")

# Quick tests
st.markdown("---")
st.subheader("🎯 Quick Tests")

test_col1, test_col2, test_col3, test_col4 = st.columns(4)

with test_col1:
    if st.button("🍚 makan", use_container_width=True):
        with st.spinner("Mencari..."):
            result = search_gayo_knowledge("makan")
            st.markdown(result)

with test_col2:
    if st.button("🏠 rumah", use_container_width=True):
        with st.spinner("Mencari..."):
            result = search_gayo_knowledge("rumah")
            st.markdown(result)

with test_col3:
    if st.button("🔧 alat", use_container_width=True):
        with st.spinner("Mencari..."):
            result = search_gayo_knowledge("alat")
            st.markdown(result)

with test_col4:
    if st.button("📖 sirih", use_container_width=True):
        with st.spinner("Mencari..."):
            result = search_gayo_knowledge("sirih")
            st.markdown(result)

# Sample entries preview
st.markdown("---")
st.subheader("📋 Preview Data")

if st.button("Tampilkan Sample Entries"):
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
            metadata = item.get('metadata', {})
            with st.expander(f"{i}. {metadata.get('gayo_word', 'Unknown')}"):
                st.write(f"**Text:** {item.get('text', '')}")
                st.write(f"**Metadata:**")
                st.json(metadata)
    else:
        st.error(f"❌ Error: {response.status_code}")

# Footer
st.markdown("---")
st.markdown(
    "**ℹ️ AI Assistant untuk melestarikan bahasa dan budaya Gayo Kabupaten Bener Meriah** • "
    "**Database:** 968 entri • **Konteks Budaya:** 73% coverage"
)
