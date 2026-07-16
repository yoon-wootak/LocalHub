/**
 * 게시글 API 모듈
 */

import http from './http'
import { mapPost, mapPosts } from './mappers/postMapper'

/**
 * 게시글 목록 조회
 * GET /api/posts
 */
export const getPosts = async (params = {}) => {
  const queryParams = {}

  if (params.keyword && params.keyword.trim()) {
    queryParams.keyword = params.keyword.trim()
  }
  if (params.category && params.category !== '전체') {
    queryParams.category = params.category
  }
  if (params.page !== undefined && params.page !== null) {
    queryParams.page = params.page
  }
  if (params.size !== undefined && params.size !== null) {
    queryParams.size = params.size
  }

  const response = await http.get('/api/posts', { params: queryParams })

  let items = []
  let total = 0
  let page = 1
  let size = 10

  if (Array.isArray(response.data)) {
    items = mapPosts(response.data)
    total = items.length
  } else if (response.data && typeof response.data === 'object') {
    if (Array.isArray(response.data.items)) {
      items = mapPosts(response.data.items)
    } else if (Array.isArray(response.data.data)) {
      items = mapPosts(response.data.data)
    }
    total = response.data.total || 0
    page = response.data.page || 1
    size = response.data.size || 10
  }

  return {
    items,
    total,
    page,
    size
  }
}

/**
 * 단일 게시글 조회
 * GET /api/posts/{id}
 */
export const getPost = async (postId) => {
  if (!postId) {
    throw new Error('게시글 ID가 필요합니다.')
  }

  const response = await http.get(`/api/posts/${postId}`)
  const post = mapPost(response.data)

  if (!post) {
    throw new Error('게시글을 찾을 수 없습니다.')
  }

  return post
}

/**
 * 게시글 작성
 * POST /api/posts
 */
export const createPost = async (payload) => {
  if (!payload.title || !payload.content || !payload.category || !payload.password) {
    throw new Error('필수 필드가 누락되었습니다.')
  }

  const data = {
    title: payload.title,
    content: payload.content,
    category: payload.category,
    password: payload.password,
    location_name: payload.locationName || null
  }

  const response = await http.post('/api/posts', data)
  const post = mapPost(response.data)

  if (!post) {
    throw new Error('게시글 생성에 실패했습니다.')
  }

  return post
}

/**
 * 게시글 수정
 * PUT /api/posts/{id}
 */
export const updatePost = async (postId, payload) => {
  if (!postId) {
    throw new Error('게시글 ID가 필요합니다.')
  }

  if (!payload.title || !payload.content || !payload.category) {
    throw new Error('필수 필드가 누락되었습니다.')
  }

  const data = {
    title: payload.title,
    content: payload.content,
    category: payload.category,
    location_name: payload.locationName || null
  }

  const response = await http.put(`/api/posts/${postId}`, data)
  const post = mapPost(response.data)

  if (!post) {
    throw new Error('게시글 수정에 실패했습니다.')
  }

  return post
}

/**
 * 게시글 삭제
 * DELETE /api/posts/{id}
 *
 * TODO: 백엔드와 DELETE 요청 형식 확인 필요
 * 현재는 body에 password를 포함하는 방식 사용
 */
export const deletePost = async (postId, password) => {
  if (!postId) {
    throw new Error('게시글 ID가 필요합니다.')
  }

  if (!password) {
    throw new Error('비밀번호가 필요합니다.')
  }

  // TODO: 백엔드 담당자와 DELETE body 형식 확인
  const response = await http.delete(`/api/posts/${postId}`, {
    data: {
      password
    }
  })

  return response.data
}

/**
 * 게시글 비밀번호 검증
 * POST /api/posts/{id}/verify-password
 *
 * 주의: 이 API가 백엔드에 구현되지 않았을 수 있습니다.
 */
export const verifyPostPassword = async (postId, password) => {
  if (!postId) {
    throw new Error('게시글 ID가 필요합니다.')
  }

  if (!password) {
    throw new Error('비밀번호가 필요합니다.')
  }

  const response = await http.post(`/api/posts/${postId}/verify-password`, {
    password
  })

  return response.data
}

/**
 * 게시글 좋아요 추가
 * POST /api/posts/{id}/like
 */
export const likePost = async (postId) => {
  if (!postId) {
    throw new Error('게시글 ID가 필요합니다.')
  }

  const response = await http.post(
    `/api/posts/${postId}/like`,
  )

  return {
    liked: response.data.liked === true,
    likeCount:
      response.data.like_count ?? 0,
  }
}


/**
 * 게시글 좋아요 취소
 * DELETE /api/posts/{id}/like
 */
export const unlikePost = async (postId) => {
  if (!postId) {
    throw new Error('게시글 ID가 필요합니다.')
  }

  const response = await http.delete(
    `/api/posts/${postId}/like`,
  )

  return {
    liked: response.data.liked === true,
    likeCount:
      response.data.like_count ?? 0,
  }
}

/**
 * 인기 게시글 조회
 * GET /api/posts/popular
 */
export const getPopularPosts = async (limit = 4) => {
  const response = await http.get('/api/posts/popular', {
    params: {
      limit
    }
  })

  return mapPosts(response.data)
}