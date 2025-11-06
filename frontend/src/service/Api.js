const BASE_URL = "http://192.168.18.80:1880"

export const Api = {
   async request(endpoint, options = {}){
    const url = `${BASE_URL}${endpoint}`
    const response = await fetch(url, {
        headers: {
        'Content-Type' : 'application/json',
        ...options.headers
    }, ...options})

    if (!response.ok)
        throw new Error (`API error: ${response.status}`)
    
    return response.json()

   }
}