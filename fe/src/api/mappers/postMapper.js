/**
 * FastAPI 응답을 Vue 화면 모델로 변환
 */

const toCamelCase = (str) => {
  return str.replace(/_([a-z])/g, (match, letter) => letter.toUpperCase())
}

const transformKeys = (obj) => {
  if (!obj || typeof obj !== 'object') return obj

  if (Array.isArray(obj)) {
    return obj.map(transformKeys)
  }

  const transformed = {}
  for (const [key, value] of Object.entries(obj)) {
    if (key === 'password') {
      continue
    }
    const camelKey = toCamelCase(key)
    if (Array.isArray(value)) {
      transformed[camelKey] = value
    } else if (typeof value === 'object' && value !== null) {
      transformed[camelKey] = transformKeys(value)
    } else {
      transformed[camelKey] = value
    }
  }
  return transformed
}

export const mapPost = (rawPost) => {
  if (!rawPost || typeof rawPost !== 'object') {
    return null
  }

  const post = transformKeys(rawPost)

return {
  id: post.id ? Number(post.id) : null,
  title: post.title || '',
  content: post.content || '',
  category: post.category || '',

  createdAt: post.createdAt || new Date().toISOString(),
  updatedAt: post.updatedAt || null,

  viewCount: Number(post.viewCount ?? 0),
  likeCount: Number(post.likeCount ?? 0),

  locationName: post.locationName || null
}
}

export const mapPosts = (rawPosts) => {
  if (!Array.isArray(rawPosts)) {
    return []
  }
  return rawPosts
    .map(mapPost)
    .filter((p) => p !== null)
}