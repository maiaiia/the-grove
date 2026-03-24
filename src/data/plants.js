import {PLANT_CATEGORIES} from "@/data/plantCategories.js";

export function createPlant(data) {
    return {
        id: data.id,
        name: data.name,
        latinName: data.latinName,
        category: data.category,
        age: data.age,
        image: data.image,
        lastWatered: data.lastWatered,
        lastPhotoDate: data.lastPhotoDate,
    }
}

export const plants=[
    createPlant({
        id: 1,
        name: "Monstera Rex",
        latinName: "Monstera deliciosa",
        category: PLANT_CATEGORIES.SUCCULENT,
        age: 3,
        image: "public/monstera.jpg",
        lastWatered: "20/03/2026",
        lastPhotoDate: "20/03/2026",
    }),
    createPlant({
        id:2,
        name: "Old Juniper",
        latinName: "Juniperus chinensis",
        category: PLANT_CATEGORIES.BONSAI,
        age: 12,
        image: "public/oldjuniper.jpeg",
        lastWatered: "24/03/2026",
        lastPhotoDate: "20/03/2026",
    }),
    createPlant({
        id: 3,
        name: "Little Ficus",
        latinName: "Ficus retusa",
        category: PLANT_CATEGORIES.BONSAI,
        age: 8,
        image: "public/ficus.jpeg",
        lastWatered: "21/03/2026",
        lastPhotoDate: "20/03/2026",
    })
]