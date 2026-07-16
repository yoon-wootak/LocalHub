<template>
  <section class="bg-[var(--color-background)] py-16">
    <div class="page-container">
      <div
        class="mb-8 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between"
      >
        <div>
          <h2 class="text-3xl font-semibold text-[var(--color-text)]">
            지금 주목할 지역의 장소
          </h2>

          <p class="mt-2 max-w-xl text-sm text-[var(--color-text-muted)]">
            추천 장소를 살펴보고 상세 정보를 확인해보세요.
          </p>
        </div>

        <RouterLink
          to="/places"
          class="inline-flex items-center gap-2 text-sm font-semibold text-[var(--color-primary)] transition hover:text-[var(--color-secondary)]"
        >
          전체 장소 보기
          <span aria-hidden="true">→</span>
        </RouterLink>
      </div>

      <!-- 실제 장소 데이터 -->
      <div
        v-if="featuredPlaces.length > 0"
        class="grid grid-cols-12 gap-6 md:auto-rows-[300px]"
      >
        <!-- 대표 장소 -->
        <RouterLink
          v-if="featuredPlaces[0]"
          :to="`/places/${featuredPlaces[0].id}`"
          class="group col-span-12 overflow-hidden rounded-[24px] border border-[var(--color-border)] bg-white transition duration-300 hover:-translate-y-1 hover:shadow-sm md:col-span-8 md:row-span-2"
        >
          <div class="relative h-[420px] overflow-hidden md:h-full">
            <img
              v-if="featuredPlaces[0].imageUrl"
              :src="featuredPlaces[0].imageUrl"
              :alt="featuredPlaces[0].name"
              class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
              @error="handleImageError(featuredPlaces[0])"
            />

            <div
              v-else
              class="flex h-full w-full items-center justify-center bg-[var(--color-surface-muted)] text-[var(--color-text-muted)]"
            >
              이미지 없음
            </div>

            <div
              class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/15 to-transparent"
            />

            <div class="absolute inset-x-6 bottom-6">
              <span
                v-if="featuredPlaces[0].category"
                class="inline-flex rounded-full bg-[var(--color-primary)] px-3 py-1 text-sm font-semibold text-white"
              >
                {{ featuredPlaces[0].category }}
              </span>

              <h3 class="mt-4 text-3xl font-semibold text-white">
                {{ featuredPlaces[0].name }}
              </h3>

              <p
                v-if="featuredPlaces[0].description"
                class="mt-3 max-w-xl line-clamp-2 text-sm leading-6 text-white/85"
              >
                {{ featuredPlaces[0].description }}
              </p>
            </div>
          </div>
        </RouterLink>

        <!-- 보조 장소 -->
        <div
          class="col-span-12 grid gap-6 md:col-span-4 md:row-span-2 md:grid-rows-2"
        >
          <RouterLink
            v-for="place in featuredPlaces.slice(1, 3)"
            :key="place.id"
            :to="`/places/${place.id}`"
            class="group grid h-full min-h-0 overflow-hidden rounded-[20px] border border-[var(--color-border)] bg-white transition duration-300 hover:-translate-y-1 hover:shadow-sm sm:grid-cols-[42%_1fr] md:grid-cols-1 md:grid-rows-[160px_1fr]"
          >
            <div class="relative min-h-[160px] overflow-hidden">
              <img
                v-if="place.imageUrl"
                :src="place.imageUrl"
                :alt="place.name"
                class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
                @error="handleImageError(place)"
              />

              <div
                v-else
                class="flex h-full w-full items-center justify-center bg-[var(--color-surface-muted)] text-sm text-[var(--color-text-muted)]"
              >
                이미지 없음
              </div>
            </div>

            <div class="flex min-h-0 flex-col justify-start px-5 py-4">
              <span
                v-if="place.category"
                class="inline-flex w-fit rounded-full bg-[var(--color-surface)] px-3 py-1 text-xs font-semibold text-[var(--color-primary)]"
              >
                {{ place.category }}
              </span>

              <h4
                class="mt-2 line-clamp-1 text-xl font-semibold text-[var(--color-text)]"
              >
                {{ place.name }}
              </h4>

              <p
                v-if="place.shortDescription"
                class="mt-2 line-clamp-2 text-sm leading-5 text-[var(--color-text-muted)]"
              >
                {{ place.shortDescription }}
              </p>
            </div>
          </RouterLink>
        </div>
      </div>

      <!-- 빈 상태 -->
      <div
        v-else
        class="rounded-2xl border border-[var(--color-border)] bg-white px-6 py-16 text-center text-[var(--color-text-muted)]"
      >
        표시할 장소가 없습니다.
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  places: {
    type: Array,
    default: () => [],
  },
})

const featuredPlaces = computed(() =>
  [...props.places]
    .filter((place) => place?.id && place?.name)
    .sort(
      (a, b) =>
        Number(b.viewCount ?? 0) -
        Number(a.viewCount ?? 0),
    )
    .slice(0, 3)
    .map((place) => ({
      ...place,
      imageUrl: place.imageUrl || null,
      description:
        place.description ||
        place.shortDescription ||
        place.address ||
        place.category ||
        '',
      shortDescription:
        place.shortDescription ||
        place.address ||
        place.category ||
        '',
    })),
)

const handleImageError = (place) => {
  place.imageUrl = null
}
</script>