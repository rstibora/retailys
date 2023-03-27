import type { PageServerLoad } from './$types'


interface Item {
    code: string
    name: string
    spare_part_codes: string[]
}


export const load = (async({ params }) => {
    const itemResponse = await fetch(`http://fastapi:8000/items/${params.code}/`)
    const itemResponseData: Item = await itemResponse.json()
    const sparePartsResponses = await Promise.all(itemResponseData.spare_part_codes.map(code => fetch(`http://fastapi:8000/items/${code}/`)))
    const sparePartsData = await Promise.all(sparePartsResponses.map(response => response.json()))
    return { item: itemResponseData, sparePartsData }

}) satisfies PageServerLoad
