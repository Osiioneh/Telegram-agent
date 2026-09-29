import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from crewai import Agent, Task, Crew

# ==========================================
# STEP 1: PASTE YOUR KEYS HERE (Keep the quotes!)
# ==========================================
os.environ["GROQ_API_KEY"] = "PASTE_YOUR_GROQ_KEY_HERE"
TELEGRAM_TOKEN = "PASTE_YOUR_TELEGRAM_TOKEN_HERE"

# ==========================================
# STEP 2: DEFINE YOUR AI AGENT
# ==========================================
research_agent = Agent(
    role='Personal Executive Assistant',
    goal='Help the user solve problems, draft text, and organize information.',
    backstory='You are a hyper-capable, polite, and practical private AI assistant.',
    verbose=True,
    llm_config={"model": "groq/llama3-70b-8192"}
)

# ==========================================
# STEP 3: TELEGRAM BOT MESSAGE HANDLER
# ==========================================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"📩 Received message: {user_text}") # Keeps logs visible on your phone screen
    
    await update.message.reply_text("🤖 Agent is thinking...")
    
    # Create the task
    task = Task(
        description=f"Respond to or complete this user request: {user_text}",
        expected_output="A helpful, direct, and clear response.",
        agent=research_agent
    )
    
    # Run the agent reasoning pipeline
    crew = Crew(agents=[research_agent], tasks=[task])
    result = crew.kickoff()
    
    # Reply back to Telegram
    await update.message.reply_text(str(result))

# ==========================================
# STEP 4: START THE SERVER PIPELINE
# ==========================================
def main():
    print("⚡ Booting up your Telegram AI Agent server...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # --- ADDED FOR RENDER FREE TIER COMPATIBILITY ---
    # This tricks Render into thinking it's a website so it stays free!
    import threading
    from http.server import SimpleHTTPRequestHandler, HTTPServer
    
    def run_dummy_server():
        port = int(os.environ.get("PORT", 10000))
        server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
        server.serve_forever()
        
    threading.Thread(target=run_dummy_server, daemon=True).start()
    # -----------------------------------------------

    print("🚀 Your Telegram Agent is now LIVE!")
    app.run_polling()

if __name__ == '__main__':
    main()
