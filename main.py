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
    
    # Tell the bot to look out for incoming texts
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Your Telegram Agent is now LIVE 24/7! You can close this tab and go to Telegram.")
    app.run_polling()

if __name__ == '__main__':
    main()
  
