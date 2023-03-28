from asyncio import Future
import io
import os
from unittest import IsolatedAsyncioTestCase, main, mock

from retailys.astra import fetch_and_store

class TestAstra(IsolatedAsyncioTestCase):
    async def test_fetch_and_store(self):
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/astra_export_xml.zip", "rb") as zipped:
            in_memory = io.BytesIO(zipped.read())
            with mock.patch("retailys.astra._fetch_zip", mock.AsyncMock(return_value=in_memory)):
                with mock.patch("retailys.astra._save_to_cache") as save_fn, mock.patch("retailys.astra._cache_empty", mock.MagicMock(return_value=True)):
                    await fetch_and_store()
                    assert save_fn.called
                    assert len(save_fn.call_args[0][0]) == 28066

if __name__ == '__main__':
    main()
