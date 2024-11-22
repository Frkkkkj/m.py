import psutil
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name)

class CPUMonitorBot:
    def init(self, threshold=80):
        self.threshold = threshold

    def get_cpu_usage(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        return cpu_percent

    def get_top_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        top_processes = sorted(processes, 
                               key=lambda x: x['cpu_percent'], 
                               reverse=True)[:5]
        return top_processes

# Telegram command handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /cpu to check CPU usage.")

def cpu(update: Update, context: CallbackContext):
    monitor = context.bot_data['monitor']
    cpu_percent = monitor.get_cpu_usage()
    
    if cpu_percent > monitor.threshold:
        response = f"⚠️ High CPU usage detected: {cpu_percent}%\nTop processes:\n"
        top_processes = monitor.get_top_processes()
        for proc in top_processes:
            response += f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%\n"
    else:
        response = f"✅ Current CPU usage is normal: {cpu_percent}%"
    
    update.message.reply_text(response)

# Main function
def main():
    # Replace 'YOUR_TOKEN_HERE' with your bot's API token
    TOKEN = "6893021876:AAEd87lWg7HePmK76fjuM5g53WWv_bTdcDY"
    
    # Create an instance of CPUMonitor
    monitor = CPUMonitorBot(threshold=80)
    
    # Set up the Telegram bot
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Add bot commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("cpu", cpu))
    
    # Share monitor instance with handlers
    dispatcher.bot_data['monitor'] = monitor

    # Start the bot
    updater.start_polling()
    updater.idle()

if name == "main":
    main()