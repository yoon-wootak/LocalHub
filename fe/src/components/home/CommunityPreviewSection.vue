<template>
  <section class="bg-[var(--color-background)] py-16">
    <div class="page-container">
      <div class="mb-6 flex items-end justify-between gap-6">
        <div>
          <h2 class="text-3xl font-semibold text-[var(--color-text)]">
            지역 이야기를 빠르게 확인해보세요
          </h2>

          <p class="max-w-2xl text-sm text-[var(--color-text-muted)] leading-7">
            지역 주민들이 남긴 이야기와 추천 정보를 뉴스 피드처럼 만나보세요.
          </p>
        </div>

        <RouterLink
          to="/posts"
          class="ml-auto inline-flex items-center gap-2 rounded-full bg-[var(--color-primary)] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[var(--color-secondary)]"
        >
          <span class="text-white">커뮤니티 전체보기</span>
          <span class="text-white">→</span>
        </RouterLink>
      </div>


      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <RouterLink
          v-for="post in displayedPosts"
          :key="post.id"
          :to="`/posts/${post.id}`"
          class="block rounded-[20px] border border-[var(--color-border)] bg-white p-5 transition hover:-translate-y-0.5 hover:shadow-sm"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="min-w-0">
              <h3
                class="text-lg font-semibold text-[var(--color-text)] line-clamp-2"
              >
                {{ post.title }}
              </h3>

              <div
                class="mt-3 flex flex-wrap gap-2 text-xs text-[var(--color-text-muted)]"
              >
                <span
                  class="rounded-full border border-[var(--color-border)] px-3 py-1"
                >
                  {{ post.category }}
                </span>

                <span>
                  조회수 {{ post.viewCount }}
                </span>

                <span>
                  {{ formatDate(post.created_at) }}
                </span>
              </div>
            </div>

            <div class="text-[var(--color-primary)]">
              →
            </div>
          </div>
        </RouterLink>
      </div>


      <div
        v-if="displayedPosts.length === 0"
        class="py-10 text-center text-sm text-[var(--color-text-muted)]"
      >
        등록된 인기 게시글이 없습니다.
      </div>
    </div>
  </section>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { getPopularPosts } from '@/api/postApi'


const displayedPosts = ref([])


const loadPopularPosts = async () => {
  try {
    const data = await getPopularPosts(4)

    displayedPosts.value = Array.isArray(data)
      ? data
      : data.items ?? []

  } catch (error) {
    console.error('인기 게시글 불러오기 실패:', error)
  }
}


const formatDate = (date) => {
  if (!date) return ''

  return new Date(date).toLocaleDateString('ko-KR')
}


onMounted(() => {
  loadPopularPosts()
})
</script>