export function createPlant(data) {
    return {
        id: data.id,
        name: data.name,
        latinName: data.latinName,
        category: data.category,
        age: data.age,
        image: data.image,
        lastWatered: data.lastWatered,
    }
}