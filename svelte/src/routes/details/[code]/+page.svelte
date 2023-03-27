<script lang="ts">
    import type { PageData } from "./$types"


    export let data: PageData
</script>

<h1>{data.item.name}</h1>
<ul>
{#each data.sparePartsData as sparePart}
    <a href={`/details/${sparePart.code}`}><li>{sparePart.code} | {sparePart.name}</li></a>
{/each}
</ul>
