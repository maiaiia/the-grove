import {setCookie, deleteCookie, getCookie} from "@/utils/cookieHelper.js";

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const GQL = `${BASE_URL}/graphql`

const toInt = (id) => parseInt(id, 10)

async function gql(query, variables = {}) {
    const token = getCookie('access_token')
    const headers = { 'Content-Type': 'application/json' }
    if (token) headers['Authorization'] = `Bearer ${token}`

    const res = await fetch(GQL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
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

const PHOTO_FIELDS = `
  id
  plantId
  url
  caption
  date
`;
const PLANT_SUMMARY_FIELDS = `
  id
  name
  latinName
  category
  lastWatered
  age
  image { ${PHOTO_FIELDS} }
`;
const PLANT_DETAIL_FIELDS = `
  ${PLANT_SUMMARY_FIELDS}
  location
  datePlanted
  photoCount
  wateringSchedule
  notes
  photos { ${PHOTO_FIELDS} }
`;

export const plantApi = {
    async getAllPlants() {
        const data = await gql(`query {
            plants { ${PLANT_SUMMARY_FIELDS} }
        }`)
        return data.plants
    },

    async getPlant(id) {
        const data = await gql(`query($id: Int!) {
          plant(plantId: $id) { ${PLANT_DETAIL_FIELDS} }          
        }`, { id: toInt(id) });
        return data.plant
    },

    async getPage(pageNumber, plantsPerPage) {
        const data = await gql(`query($p: Int!, $pp: Int!) {
            plantsPage(pageNumber: $p, plantsPerPage: $pp) {
                total
                plants { ${PLANT_SUMMARY_FIELDS} }
            }
        }`, { p: pageNumber, pp: plantsPerPage });
        return data.plantsPage;
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
        return data.statistics
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
            ${ PLANT_DETAIL_FIELDS }
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
            lastWatered: plantData.lastWatered,
        };
        const data = await gql(`mutation($id: Int!, $input: UpdatePlantInput!) {
      updatePlant(plantId: $id, input: $input) {
        ${PLANT_DETAIL_FIELDS}
      }
    }`, { id: toInt(id), input: input })
        return data.updatePlant
    },
    async addPhoto(plantId, photoData) {
        const data = await gql(`mutation($id: Int!, $url: String!, $caption: String!) {
        addPlantPhoto(plantId: $id, filename: $url, caption: $caption) {
            ${PHOTO_FIELDS}
        }
    }`, {
            id: toInt(plantId),
            url: photoData.url,
            caption: photoData.caption
        });
        return data.addPlantPhoto;
    },
    async deletePhoto(photoId) {
        const data = await gql(`mutation($id: Int!) {
      deletePhoto(photoId: $id)
    }`, { id: toInt(photoId) });
        return data.deletePhoto;
    },
}

export const authApi = {
    async login(username, password) {
        const data = await gql(`mutation($input: LoginInput!) {
            login(input: $input) {
                user { id username email role { name } }
                message
                token
            }
        }`, { input: { username, password } })

        if (data.login.token) {
            setCookie('access_token', data.login.token)
        }

        return data.login
    },

    async register(username, email, password) {
        const data = await gql(`mutation($input: RegisterInput!) {
            register(input: $input) {
                id username email role { name }
            }
        }`, { input: { username, email, password } })
        return data.register
    },

    async logout() {
        deleteCookie('access_token')
        const data = await gql(`mutation { logout }`)
        return data.logout
    },

    async checkAuth() {
        const data = await gql(`query {
            checkAuth { authenticated user { id username email role { name } } }
        }`)
        return data.checkAuth
    }
}