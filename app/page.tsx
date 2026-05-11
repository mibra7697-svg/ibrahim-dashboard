"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [executingId, setExecutingId] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false); // لحل مشكلة التوقيت

  const fetchTasks = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/tasks');
      if (res.ok) {
        const data = await res.json();
        setTasks(Array.isArray(data) ? data : []);
      }
    } catch (e) { console.log("Waiting for agent..."); }
    finally { setLoading(false); }
  };

  useEffect(() => {
    setMounted(true); // تأكيد أن المكون تم تحميله في المتصفح
    fetchTasks();
    const inv = setInterval(fetchTasks, 5000);
    return () => clearInterval(inv);
  }, []);

  const runAutonomousExecution = async (task: any) => {
    setExecutingId(task.id);
    try {
      const response = await fetch('http://localhost:8000/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          task_id: task.id,
          title: task.title,
          description: task.description
        })
      });
      const result = await response.json();
      if (result.status === "completed") {
        alert(`✅ تم الرفع بنجاح يا إبراهيم!\nالرابط: ${result.github_url}`);
        window.open(result.github_url, "_blank");
      }
    } catch (e) { alert("⚠️ حدث خطأ أثناء التنفيذ."); }
    finally { setExecutingId(null); }
  };

  return (
    <main className="p-8 bg-zinc-50 dark:bg-black min-h-screen font-sans text-right" dir="rtl">
      <div className="max-w-4xl mx-auto">
        
        {/* مؤشر العميل النشط */}
        <div className="flex justify-between items-center mb-6 bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-800">
          <div className="flex items-center gap-3">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
            <span className="text-green-700 dark:text-green-400 text-sm font-bold">العميل الذكي نشط: GLM-4.6 (تحليل عميق)</span>
          </div>
          {/* حل مشكلة التوقيت: لا يظهر إلا بعد التأكد من التحميل */}
          <span className="text-xs text-zinc-500">
            آخر تحديث للرادار: {mounted ? new Date().toLocaleTimeString('en-GB') : "--:--:--"}
          </span>
        </div>

        <header className="mb-10 border-b pb-6 border-zinc-200 dark:border-zinc-800">
          <h1 className="text-3xl font-bold text-blue-600">رادار التنفيذ - إبراهيم ياسين مرهج</h1>
          <p className="text-zinc-500 mt-2 font-medium">إدارة المهام المستقلة | Full-stack & AI Expert</p>
        </header>

        <div className="grid gap-8">
          {tasks.map((task) => (
            <div key={task.id} className="p-6 border rounded-2xl bg-white dark:bg-zinc-900 shadow-sm border-zinc-200 dark:border-zinc-800 hover:border-blue-500 transition-all hover:shadow-md">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-xl font-bold text-zinc-800 dark:text-zinc-100">{task.title}</h2>
                <span className="bg-zinc-100 dark:bg-zinc-800 text-zinc-500 text-[10px] px-2 py-1 rounded-md uppercase tracking-wider">Ref: {task.id}</span>
              </div>
              
              {/* عرض المقترح الكامل كما طلبت */}
              <div className="bg-zinc-50 dark:bg-zinc-800/40 p-5 rounded-xl mb-6 border-r-4 border-blue-500">
                <h3 className="text-sm font-bold text-blue-600 mb-3 flex items-center gap-2">
                  <span>📑</span> مراجعة المقترح الآلي:
                </h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed">
                  {task.description}
                </p>
                <div className="mt-4 pt-3 border-t border-zinc-200 dark:border-zinc-700 flex justify-between items-center text-[11px] text-zinc-400">
                   <span>توقيع العميل: إبراهيم ياسين مرهج</span>
                   <span className="bg-blue-50 dark:bg-blue-900/20 text-blue-500 px-2 py-0.5 rounded">Status: Ready to Execute</span>
                </div>
              </div>

              <div className="flex justify-between items-center">
                <a href={task.link} target="_blank" className="text-blue-500 text-sm font-medium hover:underline flex items-center gap-1">
                  المصدر الأصلي للمهمة 🔗
                </a>
                
                <button 
                  onClick={() => runAutonomousExecution(task)}
                  disabled={executingId === task.id}
                  className={`px-8 py-3 rounded-xl font-bold text-white transition-all shadow-md active:scale-95 ${
                    executingId === task.id ? 'bg-zinc-400 cursor-not-allowed animate-pulse' : 'bg-blue-600 hover:bg-blue-700'
                  }`}
                >
                  {executingId === task.id ? "⏳ جاري الرفع لـ GitHub..." : "🚀 تنفيذ ورفع فوري"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}