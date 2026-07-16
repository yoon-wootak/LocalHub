const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://localhub-u5qv.onrender.com'

export async function sendChatMessage(message) {
  const res = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  })

  const data = await res.json()
  if (!res.ok) throw new Error(data.detail ?? data.message ?? 'AI 응답을 불러오지 못했습니다.')
  return data
}