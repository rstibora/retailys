<script lang="ts">
    import type { PageData } from "./$types"


    export let data: PageData
</script>

<div class="bg-slate-200">
    Total item count: {data.items_count}

    {#each data.items as item}
        <a href={`/details/${item.code}`}><div>{item.name}</div></a>
    {/each}

    <nav class="font-bold">
        {#if data.page > 0}
            <div>
                <a href={`/items/${data.page - 1}`}>Previous</a>
            </div>
        {/if}
        {#if data.page < Math.floor(data.items_count / 10)}
            <div>
                <a href={`/items/${data.page + 1}`}>Next</a>
            </div>
        {/if}
    </nav>
</div>
