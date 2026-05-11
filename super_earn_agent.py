import os, json, time, requests, threading, subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# --- الإعدادات المعتمدة لإبراهيم ياسين مرهج ---
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

# --- وحدة مزامنة المهام ---
def sync_tasks():
    live_tasks = [
        {
            "id": "tether_qvac_palmsafe",
            "title": "Tether Frontier: PalmSafe QVAC Integration",
            "description": "Implementing QVAC SDK for local-first AI auditing and WDK for secure USDT escrow within PalmSafe.",
            "reward": "10,000 USDT",
            "deadline": "2026-05-11",
            "link": "https://earn.superteam.fun/listings/hackathon/tether-frontier/"
        },
        {
            "id": "birdeye_sprint_4",
            "title": "Birdeye Data BIP Competition — Sprint 4",
            "description": "On-chain data insights for Birdeye platform focusing on liquidity and whale movements.",
            "reward": "500 USDC",
            "deadline": "2026-05-16",
            "link": "https://earn.superteam.fun/listings/bounty/birdeye-data-bip-sprint-4/"
        }
    ]
    with open(CONFIG["db_file"], 'w', encoding='utf-8') as f:
        json.dump(live_tasks, f, ensure_ascii=False, indent=4)

# --- محرك الرفع لـ GitHub ---
def push_to_github(file_path, commit_message):
    try:
        os.chdir(CONFIG["github_repo_path"])
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "config", "user.name", CONFIG["full_name"]], check=True)
        subprocess.run(["git", "commit", "-m", commit_message, "--allow-empty"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        filename = os.path.basename(file_path)
        return f"https://github.com/{CONFIG['github_username']}/ibrahim-dashboard/blob/main/{filename}"
    except Exception as e:
        print(f"❌ GitHub Error: {e}")
        return None

# --- محرك توليد التقرير الفني لـ Birdeye ---
def generate_birdeye_report(title, description, task_id):
    print(f"📊 جاري استخراج رؤى البيانات لمهمة: {title}")
    prompt = f"""
    As a Data Analyst and Full-stack Developer, generate a professional technical report for Birdeye Sprint 4.
    Project: On-chain Market Intelligence Dashboard.
    
    Analysis Focus:
    1. Liquidity Tracking: Using Birdeye APIs to track SOL/USDC pool depth and health.
    2. Whale Monitoring: Technical methodology for detecting large wallet movements before price action.
    3. Technical Integration: How to fetch on-chain data into a Next.js dashboard.
    4. Data Verification: Ensuring accuracy using Solana RPC nodes.
    
    Format: Markdown (.md) with structured sections.
    Signature: {CONFIG['full_name']} | Data Analyst & Full-stack Developer.
    """
    try:
        payload = {"model": CONFIG["model_name"], "prompt": prompt, "stream": False}
        res = requests.post(CONFIG["ollama_url"], json=payload, timeout=600)
        content = res.json().get("response", "Data analysis failed.")
        file_name = f"ANALYSIS_{task_id}.md"
        full_path = os.path.join(CONFIG["github_repo_path"], file_name)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_name, content
    except Exception as e:
        print(f"❌ Birdeye AI Error: {e}")
        return None, None

# --- محرك توليد التقرير التقني لـ Tether ---
def generate_palmsafe_submission(title, description, task_id):
    print(f"🛠️ جاري بناء توثيق PalmSafe & QVAC: {title}")
    prompt = f"""
    Create a technical submission for Tether Frontier Hackathon.
    Project: PalmSafe (Sovereign AI Escrow).
    Focus: Integration of @qvac/sdk for local-first AI auditing on Solana.
    Format: Markdown (.md).
    Signature: {CONFIG['full_name']}
    """
    try:
        payload = {"model": CONFIG["model_name"], "prompt": prompt, "stream": False}
        res = requests.post(CONFIG["ollama_url"], json=payload, timeout=600)
        content = res.json().get("response", "Documentation failed.")
        file_name = f"SUBMISSION_{task_id}.md"
        full_path = os.path.join(CONFIG["github_repo_path"], file_name)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_name, content
    except Exception as e:
        return None, None

@app.get("/api/tasks")
async def get_tasks():
    if os.path.exists(CONFIG["db_file"]):
        with open(CONFIG["db_file"], 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.post("/submit")
async def handle_submit(req: ExecutionRequest):
    # التوجيه الذكي للمهام
    if "birdeye" in req.task_id.lower():
        file_path, content = generate_birdeye_report(req.title, req.description, req.task_id)
        commit_msg = f"Birdeye Data Insights: {req.title}"
    elif "tether" in req.task_id.lower():
        file_path, content = generate_palmsafe_submission(req.title, req.description, req.task_id)
        commit_msg = f"PalmSafe QVAC Submission: {req.title}"
    else:
        # افتراضي للمهام الأخرى
        file_path, content = generate_birdeye_report(req.title, req.description, req.task_id)
        commit_msg = f"General Submission: {req.title}"
        
    if not file_path: 
        raise HTTPException(status_code=500, detail="Generation Failed")

    github_link = push_to_github(file_path, commit_msg)
    
    return {"status": "completed", "github_url": github_link}

if __name__ == "__main__":
    sync_tasks()
    uvicorn.run(app, host="0.0.0.0", port=8000)