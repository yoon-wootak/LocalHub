<template>
  <div
    v-if="post"
    class="min-h-screen bg-[var(--color-background)]"
  >
    <main class="py-10 md:py-14">
      <div class="page-container">
        <div class="mx-auto max-w-4xl">
          <!-- 목록으로 돌아가기 -->
          <RouterLink
            to="/posts"
            class="mb-7 inline-flex items-center gap-2 text-sm font-semibold !text-[var(--color-text)] transition hover:gap-3 hover:!text-[var(--color-primary)]"
          >
            <span aria-hidden="true">←</span>
            목록으로 돌아가기
          </RouterLink>

          <!-- 게시글 -->
          <article
            class="rounded-[20px] border border-[var(--color-border)] bg-white px-8 py-8 shadow-sm md:px-10 md:py-10"
          >
            <!-- 상단 정보 -->
            <div class="relative">
              <div class="pr-12">
                <!-- 카테고리 -->
                <span
                  class="inline-flex items-center rounded-[8px] bg-blue-50 px-3 py-1.5 text-sm font-semibold text-blue-700"
                >
                  {{ post.category }}
                </span>

                <!-- 제목 -->
                <h1
                  class="mt-5 break-keep text-3xl font-bold leading-tight text-[var(--color-text)] md:text-4xl"
                >
                  {{ post.title }}
                </h1>
              </div>

              <!-- 더보기 메뉴 -->
              <div
                ref="menuRef"
                class="absolute right-0 top-0"
              >
                <button
                  type="button"
                  aria-label="게시글 관리 메뉴"
                  :aria-expanded="isMenuOpen"
                  class="flex h-10 w-10 items-center justify-center rounded-full text-2xl leading-none text-[var(--color-text-muted)] transition hover:bg-[var(--color-surface-muted)] hover:text-[var(--color-text)]"
                  @click.stop="toggleMenu"
                >
                  ⋮
                </button>

                <div
                  v-if="isMenuOpen"
                  class="absolute right-0 top-12 z-20 w-28 overflow-hidden rounded-[12px] border border-[var(--color-border)] bg-white py-1 shadow-lg"
                >
                  <button
                    type="button"
                    class="flex w-full items-center px-4 py-2.5 text-left text-sm font-medium text-[var(--color-text)] transition hover:bg-[var(--color-surface-muted)]"
                    @click="openEditModal"
                  >
                    수정
                  </button>

                  <button
                    type="button"
                    class="flex w-full items-center px-4 py-2.5 text-left text-sm font-medium text-red-500 transition hover:bg-red-50"
                    @click="openDeleteModal"
                  >
                    삭제
                  </button>
                </div>
              </div>
            </div>

            <!-- 메타 정보 -->
<div
  class="mt-6 flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-[var(--color-text-muted)]"
>
  <span>
    작성일: {{ formatDateTime(post.createdAt) }}
  </span>

  <span v-if="post.updatedAt">
    수정됨: {{ formatDateTime(post.updatedAt) }}
  </span>


  <span>
    조회수: {{ post.viewCount ?? 0 }}
  </span>


  <!-- 좋아요 -->
  <button
    type="button"
    :disabled="likeLoading"
    class="inline-flex items-center gap-1 transition hover:text-[var(--color-primary)]"
    @click="toggleLike"
  >
    <span>
      {{ liked ? '❤️' : '🤍' }}
    </span>

    <span>
      {{ post.likeCount ?? 0 }}
    </span>
  </button>


  <span
    v-if="post.locationName"
    class="inline-flex items-center gap-1"
  >
    <span aria-hidden="true">📍</span>
    {{ post.locationName }}
  </span>

</div>

            <!-- 구분선 -->
            <div class="my-8 border-t border-[var(--color-border)]"></div>

            <!-- 본문 -->
            <p
              class="min-h-[120px] whitespace-pre-wrap break-words text-base leading-8 text-[var(--color-text)]"
            >
              {{ post.content }}
            </p>
          </article>
        </div>
      </div>
    </main>

    <!-- 수정 비밀번호 모달 -->
    <PasswordModal
      :open="showEditPasswordModal"
      title="게시글 수정"
      description="이 게시글을 수정하려면 작성 시 등록한 비밀번호를 입력하세요."
      confirm-text="인증"
      :loading="editLoading"
      :error-message="editError"
      @close="closeEditModal"
      @confirm="handleEditPassword"
    />

    <!-- 삭제 비밀번호 모달 -->
    <PasswordModal
      :open="showDeletePasswordModal"
      title="게시글 삭제"
      description="삭제한 게시글은 복구할 수 없습니다. 작성 시 등록한 비밀번호를 입력하세요."
      confirm-text="삭제"
      :loading="deleteLoading"
      :error-message="deleteError"
      @close="closeDeleteModal"
      @confirm="handleDeletePassword"
    />
  </div>

  <!-- Not Found -->
  <div
    v-else
    class="flex min-h-screen items-center justify-center bg-[var(--color-background)] px-6"
  >
    <div
      class="w-full max-w-lg rounded-[24px] border border-[var(--color-border)] bg-white px-8 py-14 text-center shadow-sm"
    >
      <div
        class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-[var(--color-surface-muted)] text-2xl"
      >
        📝
      </div>

      <h1 class="mt-6 text-3xl font-bold text-[var(--color-text)]">
        게시글을 찾을 수 없습니다
      </h1>

      <p class="mt-3 text-sm leading-7 text-[var(--color-text-muted)]">
        요청하신 게시글이 없거나 삭제되었습니다.
      </p>

      <RouterLink
        to="/posts"
        class="mt-8 inline-flex h-12 items-center justify-center rounded-[14px] bg-[var(--color-primary)] px-6 text-sm font-semibold !text-white transition hover:bg-[var(--color-primary-hover)]"
      >
        목록으로 돌아가기
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import {
  onBeforeUnmount,
  onMounted,
  ref,
  computed,
} from 'vue'
import { useRoute, useRouter } from 'vue-router'

import PasswordModal from '@/components/post/PasswordModal.vue'

import {
  getPost,
  deletePost,
  verifyPostPassword,
  likePost,
  unlikePost,
} from '@/api/postApi'


const route = useRoute()
const router = useRouter()


const postId = computed(() =>
  String(route.params.id)
)

const post = ref(null)


const menuRef = ref(null)
const isMenuOpen = ref(false)


const showEditPasswordModal = ref(false)
const showDeletePasswordModal = ref(false)


const editLoading = ref(false)
const editError = ref('')


const deleteLoading = ref(false)
const deleteError = ref('')


/*
 * 좋아요 상태
 */
const liked = ref(false)
const likeLoading = ref(false)



/**
 * 게시글 좋아요 저장 키
 */
const getLikeStorageKey = (id) => {
  return `localhub:post-like:${id}`
}



/**
 * 좋아요 상태 읽기
 */
const readLikedState = (id) => {
  return (
    localStorage.getItem(
      getLikeStorageKey(id),
    ) === 'true'
  )
}



/**
 * 좋아요 상태 저장
 */
const saveLikedState = (
  id,
  isLiked,
) => {

  const key =
    getLikeStorageKey(id)


  if (isLiked) {

    localStorage.setItem(
      key,
      'true',
    )

    return
  }


  localStorage.removeItem(key)
}



/**
 * 게시글 좋아요 토글
 */
const toggleLike = async () => {

  if (
    !post.value ||
    likeLoading.value
  ) {
    return
  }


  const id = post.value.id


  const previousLiked =
    liked.value


  const previousCount =
    post.value.likeCount ?? 0



  likeLoading.value = true


  /*
   * 낙관적 업데이트
   */
  liked.value =
    !previousLiked


  post.value.likeCount =
    Math.max(
      0,
      previousCount +
        (liked.value ? 1 : -1),
    )



  try {

    const result = liked.value
      ? await likePost(id)
      : await unlikePost(id)


    liked.value =
      result.liked


    post.value.likeCount =
      result.likeCount


    saveLikedState(
      id,
      result.liked,
    )


  } catch(error) {

    console.error(
      '좋아요 처리 실패:',
      error,
    )


    /*
     * 실패 시 원상복구
     */
    liked.value =
      previousLiked


    post.value.likeCount =
      previousCount


  } finally {

    likeLoading.value = false

  }
}



/**
 * 게시글 조회
 */
const loadPost = async () => {

  try {

    post.value =
      await getPost(postId.value)


    liked.value =
      readLikedState(
        post.value.id,
      )


  } catch(error) {

    console.error(error)

  }
}



const formatDateTime = (
  dateString,
) => {

  if (!dateString) {
    return '-'
  }


  return new Date(
    dateString,
  ).toLocaleString('ko-KR')

}




const toggleMenu = () => {

  isMenuOpen.value =
    !isMenuOpen.value

}



const closeMenu = () => {

  isMenuOpen.value = false

}



const handleOutsideClick = (
  event,
) => {

  if (
    menuRef.value &&
    !menuRef.value.contains(
      event.target,
    )
  ) {

    closeMenu()

  }

}



const openEditModal = () => {

  closeMenu()

  editError.value = ''

  showEditPasswordModal.value =
    true

}



const closeEditModal = () => {

  showEditPasswordModal.value =
    false

}



const openDeleteModal = () => {

  closeMenu()

  deleteError.value = ''

  showDeletePasswordModal.value =
    true

}



const closeDeleteModal = () => {

  showDeletePasswordModal.value =
    false

}




const handleEditPassword = async (
  password,
) => {

  try {

    await verifyPostPassword(
      postId.value,
      password,
    )


    sessionStorage.setItem(
      `localhub-post-edit-${postId.value}`,
      'verified',
    )


    router.push(
      `/posts/${postId.value}/edit`,
    )


  } catch(error) {

    editError.value =
      error.message

  }

}




const handleDeletePassword = async (
  password,
) => {

  try {

    await deletePost(
      postId.value,
      password,
    )


    router.push('/posts')


  } catch(error) {

    deleteError.value =
      error.message

  }

}



onMounted(() => {

  loadPost()


  document.addEventListener(
    'click',
    handleOutsideClick,
  )

})



onBeforeUnmount(() => {

  document.removeEventListener(
    'click',
    handleOutsideClick,
  )

})

</script>