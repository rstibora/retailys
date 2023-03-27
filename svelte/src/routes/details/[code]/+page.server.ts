import type { PageServerLoad } from './$types'


interface Item {
    code: string
    name: string
    spare_part_codes: string[]
}


export const load = (async({ params }) => {
    const response = await fetch(`http://fastapi:8000/items/${params.code}/`)
    const responseData: { item: Item } = await response.json()
    return responseData
}) satisfies PageServerLoad
