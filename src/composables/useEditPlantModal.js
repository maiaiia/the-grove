import { ref } from 'vue'

const isOpen = ref(false)
const plantToEdit = ref(null)

export function useEditPlantModal() {
    const open = (plant) => {
        plantToEdit.value = plant
        isOpen.value = true
    }
    const close = () => {
        isOpen.value = false
        plantToEdit.value = null
    }
    return { isOpen, plantToEdit, open, close }
}