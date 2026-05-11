import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { taskId, proposal } = body;

    // إرسال الطلب إلى وكيل البايثون ليقوم بعملية الـ Submission الرسمية
    // الوكيل سيتولى التعامل مع الـ API Key والـ Signatures المطلوبة
    const pythonAgentRes = await fetch('http://localhost:8000/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        task_id: taskId,
        proposal_text: proposal
      })
    });

    if (pythonAgentRes.ok) {
      return NextResponse.json({ success: true });
    } else {
      return NextResponse.json({ success: false }, { status: 500 });
    }
  } catch (error) {
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}