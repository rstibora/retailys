import type { PageServerLoad } from './$types'


interface Item {
    code: string
    name: string
}


export const load = (async({ params }) => {
    let page = parseInt(params.page)
    if (page === undefined) {
        page = 0
    }
    const response = await fetch(`http://fastapi:8000/items/?items_from=${page * 10}&items_to=${((page + 1) * 10) - 1}`)
    const responseData: { items: Item[], items_count: number, page: number} = { page, ...await response.json()}
    return responseData
}) satisfies PageServerLoad
