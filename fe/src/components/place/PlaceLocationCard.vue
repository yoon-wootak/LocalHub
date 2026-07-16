<template>
  <div class="sticky top-[calc(var(--header-height)+24px)] space-y-6">
    <div class="rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm">
      <h3 class="text-lg font-semibold text-[var(--color-text)]">위치</h3>

      <p class="mt-2 text-sm text-[var(--color-text-muted)] line-clamp-3">
        {{ place.address || '주소 정보 없음' }}
      </p>

      <div class="mt-4">
        <PlaceMap
          :places="[place]"
          :selected-place-id="place.id"
          :center="[place.latitude, place.longitude]"
          :zoom="15"
          map-height="280px"
        />
      </div>

      <div class="mt-4 flex gap-2">
        <a
          v-if="destinationUrl"
          :href="destinationUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="flex-1 rounded-lg bg-[var(--color-primary)] px-4 py-3 text-center font-semibold !text-white transition hover:bg-[var(--color-primary-hover)] hover:!text-white"
        >
          길찾기
        </a>

        
      </div>
    </div>

    <RouterLink
      to="/places"
      class="block rounded-lg border border-[var(--color-border)] bg-white px-4 py-3 text-center text-[var(--color-text)] font-semibold shadow-sm"
    >
      목록으로 돌아가기
    </RouterLink>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import PlaceMap from '@/components/place/PlaceMap.vue'

const props = defineProps({
  place: { type: Object, required: true },
})

const destinationUrl = computed(() => {
  if (!props.place?.latitude || !props.place?.longitude) {
    return ''
  }

  return `https://www.openstreetmap.org/?mlat=${props.place.latitude}&mlon=${props.place.longitude}&zoom=15`
})
</script>