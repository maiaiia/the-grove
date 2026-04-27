const BASE_URL = 'http://localhost:8000'
const GQL = `${BASE_URL}/graphql`

const toInt = (id) => parseInt(id, 10)

async function gql(query, variables = {}) {
    const res = await fetch(GQL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, variables }),
    })
    const json = await res.json()
    if (json.errors) throw new Error(json.errors[0].message)
    return json.data
}

export const checkNetworkStatus = async () => {
    if (!navigator.onLine) return false
    try {
        const res = await fetch(`${BASE_URL}/api/health`, {
            method: 'HEAD',
            signal: AbortSignal.timeout(3000)
        })
        return res.ok
    } catch {
        return false
    }
}

export const plantApi = {
    async getAllPlants() {
        const data = await gql(`query {
      plants { id name latinName category lastWatered age
        image { url caption date }
      }
    }`)
        return data.plants
    },

    async getPlant(id) {
        const data = await gql(`query($id: Int!) {
      plant(plantId: $id) {
        id name latinName category lastWatered age
        location datePlanted photoCount wateringSchedule notes
        image { url caption date }
        photos { url caption date }
      }
    }`, { id: toInt(id) })
        return data.plant
    },

    async getPage(pageNumber, plantsPerPage) {
        const data = await gql(`query($p: Int!, $pp: Int!) {
      plantsPage(pageNumber: $p, plantsPerPage: $pp) {
        total
        plants { id name latinName category lastWatered age
          image { url caption date }
        }
      }
    }`, { p: pageNumber, pp: plantsPerPage })
        return data.plantsPage   // has .total and .plants — same shape the store expects
    },

    async getStats() {
        const data = await gql(`query {
      statistics {
        totalPlants oldestPlant totalPhotos uniqueLocations
        ageDistribution      { label count }
        typeDistribution     { label count }
        photoDistribution    { label count }
        wateringDistribution { label count }
        locationDistribution { label count }
      }
    }`)
        return data.statistics   // store accesses data.totalPlants etc. directly — still works
    },

    async addPlant(plantData) {
        const input = {
            name: plantData.name,
            latinName: plantData.latinName,
            category: plantData.category,
            location: plantData.location,
            datePlanted: plantData.datePlanted,
            wateringSchedule: plantData.wateringSchedule,
        }
        const data = await gql(`mutation($input: CreatePlantInput!) {
      createPlant(input: $input) {
        id name latinName category lastWatered age
        location datePlanted photoCount wateringSchedule notes
        image { url caption date }
        photos { url caption date }
      }
    }`, { input })
        return data.createPlant
    },

    async deletePlant(id) {
        await gql(`mutation($id: Int!) {
      deletePlant(plantId: $id)
    }`, { id: toInt(id) })
    },

    async updatePlant(updatedData) {
        const { id, ...plantData } = updatedData
        const input = {
            name: plantData.name,
            latinName: plantData.latinName,
            category: plantData.category,
            location: plantData.location,
            datePlanted: plantData.datePlanted,
            wateringSchedule: plantData.wateringSchedule,
            notes: plantData.notes,
            photos: plantData.photos,
            lastWatered: plantData.lastWatered,
        };
        const data = await gql(`mutation($id: Int!, $input: UpdatePlantInput!) {
      updatePlant(plantId: $id, input: $input) {
        id name latinName category lastWatered age
        location datePlanted photoCount wateringSchedule notes
        image { url caption date }
        photos { url caption date }
      }
    }`, { id: toInt(id), input: input })
        return data.updatePlant
    }
}