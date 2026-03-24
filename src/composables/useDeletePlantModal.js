import { ref } from 'vue'

const isOpen = ref(false)
const plantToDelete = ref(null)

export function useDeletePlantModal() {
    const open = (plant) => {
        plantToDelete.value = plant
        isOpen.value = true
    }
    const close = () => {
        isOpen.value = false
        plantToDelete.value = null
    }
    return { isOpen, plantToDelete, open, close }
}