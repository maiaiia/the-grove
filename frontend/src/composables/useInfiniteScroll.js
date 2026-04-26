import { onMounted, onUnmounted, ref, isRef } from 'vue'

export function useInfiniteScroll(callback, options = {}) {
    // 1. Accept a ref or a selector
    const { threshold = 100, target } = options
    const isFetching = ref(false)
    const hasMore = ref(true) // To stop when FastAPI returns no more data

    const handleScroll = () => {
        // Don't trigger if already loading or no more data
        if (isFetching.value || !hasMore.value) return

        const element = isRef(target) ? target.value : document.querySelector(target)
        if (!element) return

        const { scrollTop, scrollHeight, clientHeight } = element
        const distanceFromBottom = scrollHeight - (scrollTop + clientHeight)

        if (distanceFromBottom < threshold) {
            isFetching.value = true

            // Expected callback to return true/false based on more data
            Promise.resolve(callback()).then((result) => {
                // If your backend returns empty, pass 'false' to result
                hasMore.value = result !== false
            }).finally(() => {
                isFetching.value = false
            })
        }
    }

    onMounted(() => {
        const element = isRef(target) ? target.value : document.querySelector(target)
        if (element) element.addEventListener('scroll', handleScroll)
    })

    onUnmounted(() => {
        const element = isRef(target) ? target.value : document.querySelector(target)
        if (element) element.removeEventListener('scroll', handleScroll)
    })

    return { isFetching, hasMore }
}