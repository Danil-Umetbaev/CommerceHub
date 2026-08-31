from typing import Any

import httpx
from fastapi import HTTPException, status, Response

def _upstream_error(response: httpx.Response) -> HTTPException:
    try: detail = response.json()
    except ValueError:
        detail = response.text or response.reason_phrase

    return HTTPException(status_code=response.status_code, detail=detail)

async def request_service(
    method: str,
    url: str,
    json_data: Any | None = None,
    headers: dict | None = None,
    fastapi_response: Response| None = None
):
    print(">>> REQUEST TO:", url)

    async with httpx.AsyncClient(trust_env=False) as client:
        try:
            upstream_response = await client.request(
                method,
                url,
                json=json_data,
                headers=headers
            )
            if fastapi_response is not None:
                for cookie in upstream_response.headers.get_list("set-cookie"):
                    fastapi_response.raw_headers.append(
                        (b"set-cookie", cookie.encode("latin-1"))
                    )


        except httpx.RequestError as e:
            print("!!! HTTPX ERROR !!!")
            print("TYPE:", type(e))
            print("ERROR:", repr(e))
            print("URL:", e.request.url)

            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )

    if upstream_response.status_code >= 400:
        raise _upstream_error(upstream_response)

    return upstream_response.json()