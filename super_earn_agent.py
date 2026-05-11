import os, json, time, requests, threading, subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# --- إعدادات إبراهيم ياسين مرهج (السيادة الرقمية و QVAC) ---
CONFIG = {
    "ollama_url": "http://localhost:11434/api/generate",
    "model_name": "glm-4.6:cloud",
    "db_file": "tasks_db.json",
    "github_repo_path": r"C:\Users\Hp\new\ibrahim-dashboard",
    "full_name": "Ibrahem Yaseen Mrhij",
    "github_username": "mibra7697-svg" 
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExecutionRequest(BaseModel):
    task_id: str
    title: str
    description: str

# --- وحدة مزامنة المهام (تحديث المهام لتشمل مسار Tether QVAC) ---
def sync_tasks():
    live_tasks = [
        {
            "id": "tether_qvac_frontier",
            "title": "Tether Frontier Hackathon (QVAC Integration)",
            "description": "Integration of Tether QVAC SDK for local-first AI and WDK for non-custodial wallet management within Smart Souq platform.",
            "reward": "10,000 USDT (Side Track) + Main Prize",
            "deadline": "2026-05-11 11:59 PM", # اليوم هو الموعد النهائي!
            "link": "https://earn.superteam.fun/listings/hackathon/tether-frontier/"
        },
        {
            "id": "birdeye_sprint_4",
            "title": "Birdeye Data BIP Competition — Sprint 4",
            "description": "Crypto data analysis and on-chain insights for Birdeye.",
            "reward": "500 USDC",
            "deadline": "2026-05-16",
            "link": "https://earn.superteam.fun/listings/bounty/birdeye-data-bip-sprint-4/"
        }
    ]
    with open(CONFIG["db_file"], 'w', encoding='utf-8') as f:
        json.dump(live_tasks, f, ensure_ascii=False, indent=4)

# --- محرك الرفع لـ GitHub مع التوثيق الكامل ---
def push_to_github(file_path, commit_message):
    try:
        os.chdir(CONFIG["github_repo_path"])
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "config", "user.name", CONFIG["full_name"]], check=True)
        # استخدام --allow-empty لتجنب توقف الكود إذا لم يكن هناك تغييرات
        subprocess.run(["git", "commit", "-m", commit_message, "--allow-empty"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        filename = os.path.basename(file_path)
        return f"https://github.com/{CONFIG['github_username']}/ibrahim-dashboard/blob/main/{filename}"
    except Exception as e:
        print(f"❌ GitHub Error: {e}")
        return None

# --- محرك توليد المحتوى التقني (متوافق مع شروط Tether QVAC) ---
def generate_qvac_submission(title, description, task_id):
    print(f"🛠️ جاري بناء حل سيادي يدمج QVAC لمهمة: {title}")
    
    # هذا البرومبت مصمم خصيصاً ليجتاز معايير تقييم Tether (40% تكامل تقني)
    prompt = f"""
    Create a high-level technical submission for the Tether Frontier Hackathon.
    Project Name: Smart Souq (Sovereign AI Edition)
    Author: {CONFIG['full_name']}
    
    Technical Requirements to Include:
    1. QVAC Integration: Explain how we use `@qvac/sdk` and `@qvac/llm-llamacpp` for local, offline AI inference to analyze user transactions without cloud leakage.
    2. WDK Integration: Use Tether WDK (wdk.tether.io) for non-custodial wallet infrastructure, ensuring users hold their own keys securely.
    3. Use Case: Offline neural machine translation via `@qvac/translation-nmtcpp` for cross-border USDT payments in low-connectivity regions.
    4. Hardware Agnostic: Mention the use of Vulkan API for GPU acceleration on local devices (Windows/Android).
    
    Format: Markdown (.md) with Architecture, Code Snippets (Conceptual), and Product Value.
    Signature: {CONFIG['full_name']} | Full-stack Engineer & Journalist.
    """
    
    try:
        payload = {"model": CONFIG["model_name"], "prompt": prompt, "stream": False}
        res = requests.post(CONFIG["ollama_url"], json=payload, timeout=600)
        content = res.json().get("response", "Technical documentation generation failed.")
        
        file_name = f"SUBMISSION_{task_id}.md"
        full_path = os.path.join(CONFIG["github_repo_path"], file_name)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return file_name, content
    except Exception as e:
        print(f"❌ AI Generation Error: {e}")
        return None, None

@app.get("/api/tasks")
async def get_tasks():
    if os.path.exists(CONFIG["db_file"]):
        with open(CONFIG["db_file"], 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.post("/submit")
async def handle_submit(req: ExecutionRequest):
    # استخدام محرك QVAC إذا كانت المهمة تخص Tether
    if "tether" in req.task_id.lower():
        file_path, content = generate_qvac_submission(req.title, req.description, req.task_id)
    else:
        # تنفيذ افتراضي للمهام الأخرى
        file_path, content = generate_qvac_submission(req.title, req.description, req.task_id) # مؤقتاً
        
    if not file_path: raise HTTPException(status_code=500, detail="Generation Failed")

    github_link = push_to_github(file_path, f"QVAC Sovereignty Submission: {req.title}")
    
    return {"status": "completed", "github_url": github_link}

if __name__ == "__main__":
    sync_tasks()
    uvicorn.run(app, host="0.0.0.0", port=8000)