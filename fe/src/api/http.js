import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'https://localhub-u5qv.onrender.com'

if (!baseURL) {
  throw new Error(
    'VITE_API_BASE_URL 환경변수가 설정되지 않았습니다.',
  )
}

const http = axios.create({
  baseURL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 응답 인터셉터
http.interceptors.response.use(
  (response) => response,
  (error) => {
    const apiError = new Error()

    if (error.response) {
      // 서버 응답 오류
      apiError.status = error.response.status
      apiError.data = error.response.data

      // 오류 메시지 우선순위
      const message =
        error.response.data?.detail ||
        error.response.data?.message ||
        `요청 처리에 실패했습니다. (${error.response.status})`

      apiError.message = message
    } else if (error.request) {
      // 요청은 했으나 응답 없음
      apiError.message = '서버에 연결할 수 없습니다. 네트워크를 확인해주세요.'
    } else {
      // 요청 구성 오류
      apiError.message = error.message || '알 수 없는 오류가 발생했습니다.'
    }

    throw apiError
  }
)

export const getApiErrorMessage = (error, fallbackMessage = '요청 처리에 실패했습니다.') => {
  if (error instanceof Error) {
    return error.message || fallbackMessage
  }
  return fallbackMessage
}

export default http