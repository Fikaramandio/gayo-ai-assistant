import gradio as gr
import requests

SUPABASE_URL = "https://reiayveqbmlvnsfkxcal.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJlaWF5dmVxYm1sdm5zZmt4Y2FsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE4ODc0MjYsImV4cCI6MjA3NzQ2MzQyNn0.HYRXvPcX5Ttn18wuYpfSLoVBUoM6-2y1V1w3iBuUhVw"

def search_gayo(query):
    if not query or len(query) < 2:
        return "Masukkan minimal 2 karakter"
    
    try:
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        url = f"{SUPABASE_URL}/rest/v1/gayo_knowledge_base"
        params = {"or": f"(gayo_word.ilike.%{query}%,indonesian_meaning.ilike.%{query}%)", "limit": 6}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            results = response.json()
            if results:
                output = f"🔍 **Ditemukan {len(results)} hasil untuk '{query}':**\n\n"
                for i, item in enumerate(results, 1):
                    cultural_flag = " 🏛️" if item.get('cultural_context') else ""
                    output += f"{i}. **{item.get('gayo_word', 'N/A')}**{cultural_flag}\n"
                    output += f"   {item.get('indonesian_meaning', 'N/A')}\n\n"
                return output
            return "❌ Tidak ditemukan hasil"
        return "❌ Error mengakses database"
    except Exception as e:
        return f"❌ Error: {str(e)}"

iface = gr.Interface(
    fn=search_gayo,
    inputs=gr.Textbox(label="🔍 Cari Bahasa Gayo", placeholder="contoh: makan, rumah, adat..."),
    outputs=gr.Markdown(),
    title="🤖 AI Assistant Bahasa Gayo - Bener Meriah",
    description="Database: 968 entri | Konteks Budaya: 73% coverage"
)

if __name__ == "__main__":
    iface.launch()