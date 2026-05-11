import os, json, time, requests, threading, subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# --- الإعدادات المعتمدة لإبراهيم (PalmSafe & Tether Frontier) ---
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

# --- مزامنة المهام: تركيز كامل على PalmSafe و QVAC اليوم ---
def sync_tasks():
    live_tasks = [
        {
            "id": "tether_qvac_palmsafe",
            "title": "Tether Frontier: PalmSafe QVAC Integration",
            "description": "Implementing QVAC SDK for local-first AI auditing and WDK for secure USDT escrow within the PalmSafe protocol.",
            "reward": "10,000 USDT Side Track",
            "deadline": "2026-05-11 11:59 PM", # الموعد النهائي اليوم!
            "link": "https://earn.superteam.fun/listings/hackathon/tether-frontier/"
        },
        {
            "id": "birdeye_sprint_4",
            "title": "Birdeye Data BIP Competition — Sprint 4",
            "description": "On-chain data insights for Birdeye platform.",
            "reward": "500 USDC",
            "deadline": "2026-05-16",
            "link": "https://earn.superteam.fun/listings/bounty/birdeye-data-bip-sprint-4/"
        }
    ]
    with open(CONFIG["db_file"], 'w', encoding='utf-8') as f:
        json.dump(live_tasks, f, ensure_ascii=False, indent=4)

# --- محرك الرفع لـ GitHub (التوثيق الرسمي لـ PalmSafe) ---
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

# --- محرك توليد المحتوى التقني: متخصص في PalmSafe و QVAC ---
def generate_palmsafe_submission(title, description, task_id):
    print(f"🛠️ جاري بناء توثيق PalmSafe المدمج مع QVAC: {title}")
    
    # البرومبت المحدث ليعكس هوية PalmSafe في كولوسيوم
    prompt = f"""
    Create a professional technical submission for the Tether Frontier Hackathon.
    Project Name: PalmSafe (Sovereign AI Escrow Edition)
    Identity: This project is officially registered in the Colosseum Frontier Hackathon.
    Author: {CONFIG['full_name']}
    
    Key Points to include (Tether Track):
    1. Local AI Auditing: Detail how PalmSafe uses `@qvac/sdk` and `@qvac/llm-llamacpp` to audit freelance deliverables locally on the user's device via Vulkan API.
    2. USDT Escrow: Explain that Tether (USDT) is the primary stablecoin used for the escrow vault, managed via Tether WDK (wdk.tether.io).
    3. Sovereign Intelligence: Focus on privacy. Data never leaves the device.
    4. Offline Capability: Use `@qvac/translation-nmtcpp` for offline contract translation, perfect for regions with unstable internet like Syria.
    
    Format: Markdown (.md) with System Architecture and Technical Impact.
    Signature: {CONFIG['full_name']} | Full-stack Engineer & Journalist.
    """
    
    try:
        payload = {"model": CONFIG["model_name"], "prompt": prompt, "stream": False}
        res = requests.post(CONFIG["ollama_url"], json=payload, timeout=600)
        content = res.json().get("response", "Documentation failed.")
        
        file_name = f"SUBMISSION_tether_qvac_frontier.md"
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
    # تنفيذ منطق PalmSafe لمهام Tether
    if "tether" in req.task_id.lower():
        file_path, content = generate_palmsafe_submission(req.title, req.description, req.task_id)
    else:
        file_path, content = generate_palmsafe_submission(req.title, req.description, req.task_id)
        
    if not file_path: raise HTTPException(status_code=500, detail="Generation Failed")

    github_link = push_to_github(file_path, f"PalmSafe QVAC Integration: {req.title}")
    
    return {"status": "completed", "github_url": github_link}

if __name__ == "__main__":
    sync_tasks()
    uvicorn.run(app, host="0.0.0.0", port=8000)