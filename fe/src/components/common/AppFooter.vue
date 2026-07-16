<template>
  <footer class="bg-[var(--color-primary)] text-white">
    <div class="py-6 md:py-7 lg:py-8">
      <div class="page-container">
        <!-- 상단 영역 -->
        <div
          class="grid grid-cols-1 items-start gap-8 lg:grid-cols-3 lg:gap-12"
        >
          <div class="max-w-md">
            <div class="text-2xl font-bold">
              LocalHub
            </div>

            <p class="mt-4 text-base leading-7 text-white/80">
              구미의 지역 정보와 이야기를 한곳에서 만나보세요.
            </p>
          </div>

          <nav
            aria-label="푸터 메뉴"
            class="flex flex-wrap gap-x-6 gap-y-3 lg:col-span-2 lg:justify-end"
          >
            <RouterLink
              to="/"
              class="text-sm font-medium !text-white/90 transition hover:!text-white"
            >
              홈
            </RouterLink>

            <RouterLink
              to="/places"
              class="text-sm font-medium !text-white/90 transition hover:!text-white"
            >
              장소 둘러보기
            </RouterLink>

            <RouterLink
              to="/posts"
              class="text-sm font-medium !text-white/90 transition hover:!text-white"
            >
              커뮤니티
            </RouterLink>
          </nav>
        </div>

        <!-- 하단 영역 -->
        <div
          class="mt-10 flex flex-col gap-4 border-t border-white/20 pt-7 sm:flex-row sm:items-center sm:justify-between"
        >
          <p class="max-w-3xl text-sm leading-6 text-white/70">
            제공되는 정보는 공공데이터를 기반으로 하며 실제 운영 정보와 다를 수
            있습니다.
          </p>

          <p class="shrink-0 text-sm text-white/70">
            SSAFY 팀 프로젝트
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>