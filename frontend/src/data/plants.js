import {PLANT_CATEGORIES, PLANT_LOCATIONS} from "@/data/plantCategories.js";

export function createPlant(data) {
    return {
        id: data.id,
        name: data.name,
        latinName: data.latinName,
        category: data.category,
        datePlanted: data.datePlanted, //YYYY-MM-DD
        photos: data.photos ?? [],
        wateringSchedule: data.wateringSchedule,
        lastWatered: data.lastWatered ?? data.datePlanted,
        location: data.location,
        notes: data.notes ?? "",

        get age() {
            const start = new Date(this.datePlanted)
            const now = new Date()
            return Math.floor((now - start) / (1000 * 60 * 60 * 24 * 365))
        },
        get sortedPhotos() {
            return [...this.photos].sort((a, b) => a.date.localeCompare(b.date))
        },
        get latestPhoto() {
            if (!this.photos || !this.photos.length) return null
            return this.sortedPhotos[this.photos.length-1]
        },
        get image() { //TODO - refactor
            if (this.latestPhoto)
                return this.latestPhoto.url
            return null
        }
    }
}

export const plants = [
    createPlant({
        id: 1,
        name: "Monstera Rex",
        latinName: "Monstera deliciosa",
        category: PLANT_CATEGORIES.TROPICAL,
        datePlanted: "2023-03-01",
        photos: [
            { date: "2024-03-02", url: "/monstera.jpg", caption: "Looking particularly gorgeous today!" }
        ],
        wateringSchedule: 2,
        lastWatered: "2026-03-20",
        location: PLANT_LOCATIONS.WINDOWSILL,
        notes: "Grew from a single node cutting. Now has over 12 large leaves with beautiful fenestration."
    }),
    createPlant({
        id: 2,
        name: "Old Juniper",
        latinName: "Juniperus chinensis",
        category: PLANT_CATEGORIES.BONSAI,
        datePlanted: "2014-03-01",
        photos: [{ date: "2026-03-20", url: "/oldjuniper.jpeg", caption: ""  }],
        wateringSchedule: 2,
        lastWatered: "2026-03-24",
        location: PLANT_LOCATIONS.INDOORS,
    }),
    createPlant({
        id: 3,
        name: "Little Ficus",
        latinName: "Ficus retusa",
        category: PLANT_CATEGORIES.BONSAI,
        datePlanted: "2018-03-01",
        photos: [{ date: "2026-03-20", url: "/ficus.jpeg", caption: ""  }],
        wateringSchedule: 7,
        lastWatered: "2026-03-21",
        location: PLANT_LOCATIONS.INDOORS,
    }),
    createPlant({
        id: 6,
        name: "Aloe Vera",
        latinName: "Aloe vera",
        category: PLANT_CATEGORIES.SUCCULENT,
        datePlanted: "2021-03-01",
        photos: [{ date: "2026-03-20", url: "/aloevera.jpeg", caption: ""  }],
        wateringSchedule: 14,
        lastWatered: "2026-03-21",
        location: PLANT_LOCATIONS.OUTDOORS,
    }),
    createPlant({
        id: 5,
        name: "Ghost Orchid",
        latinName: "Phalaenopsis amabilis",
        category: PLANT_CATEGORIES.FLOWERING,
        datePlanted: "2024-03-01",
        photos: [{ date: "2026-03-20", url: "/ghostorchid.jpeg", caption: ""  }],
        wateringSchedule: 7,
        lastWatered: "2026-03-21",
        location: PLANT_LOCATIONS.INDOORS,
    }),
    createPlant({
        id: 4,
        name: "Black Pine",
        latinName: "Pinus thunbergii",
        category: PLANT_CATEGORIES.BONSAI,
        datePlanted: "2011-03-01",
        photos: [{ date: "2026-03-20", url: "/blackpine.jpeg", caption: ""  }],
        wateringSchedule: 2,
        lastWatered: "2026-03-21",
        location: PLANT_LOCATIONS.OUTDOORS,
    }),
]