import asyncio
from typing import List

import pytest
from bson import ObjectId
from httpx import AsyncClient, QueryParams

from mof.user.dto.user_dto import UserDTO
from mof.user.errors import user_errors
from mof.user.models.user_doc import UserDocument
from mof.user.tests.data import *


def parse_phone(phone: str) -> str:
    return (phone
            .replace('tel:', '', 1)
            .replace('-', ' ', 1)
            .replace('-', ''))


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    _user_data = user_data[0].copy()
    response = await client.post("/api/v1/users", json=_user_data)
    assert response.status_code == 200
    body = response.json()
    assert body.get("id")
    assert body.get("email") == _user_data.get("email")
    assert body.get("firstName") == _user_data.get("firstName")
    assert body.get("lastName") == _user_data.get("lastName")
    assert body.get("role") == _user_data.get("role")
    assert parse_phone(body.get("phone")) == _user_data.get("phone")
    assert body.get("deactivated") == False


@pytest.mark.asyncio
async def test_create_user_invalid_email(client: AsyncClient) -> None:
    _user_data = user_data[0].copy()
    for email in test_emails:
        await UserDocument.delete_all()
        _user_data["email"] = email
        response = await client.post("/api/v1/users", json=_user_data)
        assert response.status_code == 422
        body = response.json()
        detail = body.get("detail")
        assert detail[0].get("loc")[1] == "email"


@pytest.mark.asyncio
async def test_create_user_no_duplicate_emails(client: AsyncClient) -> None:
    _user_data = user_data[0].copy()
    response = await client.post("/api/v1/users", json=_user_data)
    assert response.status_code == 200
    response = await client.post("/api/v1/users", json=_user_data)
    assert response.status_code == user_errors.email_exists.status_code
    body = response.json()
    assert body.get("code") == user_errors.email_exists.code
    assert body.get("message") == user_errors.email_exists.message


@pytest.mark.asyncio
async def test_create_user_invalid_first_name(client: AsyncClient) -> None:
    _user_data = user_data[0].copy()
    for name in test_names:
        await UserDocument.delete_all()
        _user_data["firstName"] = name
        response = await client.post("/api/v1/users", json=_user_data)
        assert response.status_code == 422
        body = response.json()
        detail = body.get("detail")
        assert detail[0].get("loc")[1] == "firstName"


@pytest.mark.asyncio
async def test_create_user_invalid_last_name(client: AsyncClient) -> None:
    _user_data = user_data[0].copy()
    for name in test_names:
        await UserDocument.delete_all()
        _user_data["lastName"] = name
        response = await client.post("/api/v1/users", json=_user_data)
        assert response.status_code == 422
        body = response.json()
        detail = body.get("detail")
        assert detail[0].get("loc")[1] == "lastName"


@pytest.mark.asyncio
async def test_create_user_invalid_role(client: AsyncClient) -> None:
    _user_data = user_data[0].copy()
    _user_data["role"] = "INVALID_ROLE"
    response = await client.post("/api/v1/users", json=_user_data)
    assert response.status_code == 422
    body = response.json()
    detail = body.get("detail")
    assert detail[0].get("loc")[1] == "role"


@pytest.mark.asyncio
async def test_create_user_invalid_phone(client: AsyncClient) -> None:
    _user_data = user_data[0].copy()
    _user_data["phone"] = "71427429"
    response = await client.post("/api/v1/users", json=_user_data)
    assert response.status_code == 422
    body = response.json()
    detail = body.get("detail")
    assert detail[0].get("loc")[1] == "phone"


@pytest.mark.asyncio
async def test_create_user_no_duplicate_phone(client: AsyncClient) -> None:
    _user_data = user_data[0].copy()
    response = await client.post("/api/v1/users", json=_user_data)
    assert response.status_code == 200
    _user_data["email"] = "abbas.mj.srour@gmail.com"
    response = await client.post("/api/v1/users", json=_user_data)
    assert response.status_code == user_errors.email_exists.status_code
    body = response.json()
    assert body.get("code") == user_errors.phone_exists.code
    assert body.get("message") == user_errors.phone_exists.message


@pytest.mark.asyncio
async def test_create_user_invalid_password(client: AsyncClient) -> None:
    _user_data = user_data[0].copy()
    for password in test_passwords:
        await UserDocument.delete_all()
        _user_data["password"] = password
        response = await client.post("/api/v1/users", json=_user_data)
        assert response.status_code == user_errors.invalid_password.status_code
        body = response.json()
        assert body.get("code") == user_errors.invalid_password.code
        assert body.get("message") == user_errors.invalid_password.message


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient) -> None:
    _user_data = user_data[0].copy()
    response = await client.post("/api/v1/users", json=_user_data)
    assert response.status_code == 200
    body = response.json()
    id = body.get("id")

    response = await client.get(f"/api/v1/users/{id}")
    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == id
    assert body.get("email") == _user_data["email"]
    assert body.get("firstName") == _user_data["firstName"]
    assert body.get("lastName") == _user_data["lastName"]
    assert body.get("role") == _user_data["role"]
    assert parse_phone(body.get("phone")) == _user_data["phone"]


@pytest.mark.asyncio
async def test_get_user_not_exist(client: AsyncClient) -> None:
    id = ObjectId()
    response = await client.get(f"/api/v1/users/{id}")
    body = response.json()
    assert response.status_code == user_errors.not_found.status_code
    assert body.get("code") == user_errors.not_found.code
    assert body.get("message") == user_errors.not_found.message


@pytest.mark.asyncio
async def test_get_user_invalid_id(client: AsyncClient) -> None:
    id = "INVALID_ID"
    response = await client.get(f"/api/v1/users/{id}")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient) -> None:
    # setup
    async def create_user_and_assert(_user_data):
        res = await client.post("/api/v1/users", json=_user_data)
        assert res.status_code == 200

    tasks = [create_user_and_assert(data) for data in user_data]
    await asyncio.gather(*tasks)

    # check request
    request = "/api/v1/users"
    response = await client.get(request)
    assert response.status_code == 200
    body = response.json()
    items = body.get("items")
    assert len(items) == len(user_data)


@pytest.mark.asyncio
async def test_get_user_pages(client: AsyncClient) -> None:
    # setup
    async def create_user_and_assert(_user_data):
        res = await client.post("/api/v1/users", json=_user_data)
        assert res.status_code == 200

    tasks = [create_user_and_assert(data) for data in user_data]
    await asyncio.gather(*tasks)

    # check page options
    request = "/api/v1/users"
    req_size = 5
    params = QueryParams(size=req_size)
    response = await client.get(request, params=params)
    body = response.json()
    items = body.get("items")
    size = body.get("size")
    pages = body.get("pages")
    total = body.get("total")

    assert response.status_code == 200
    assert len(items) == req_size
    assert req_size == size
    assert pages * size == total


@pytest.mark.asyncio
async def test_get_users_sort(client: AsyncClient) -> None:
    # setup
    async def create_user_and_assert(_user_data):
        res = await client.post("/api/v1/users", json=_user_data)
        assert res.status_code == 200

    tasks = [create_user_and_assert(data) for data in user_data]
    await asyncio.gather(*tasks)

    # check sort
    request = "/api/v1/users"
    response = await client.get(request)
    body = response.json()
    items: List[UserDTO] = body.get("items")

    is_sorted = True

    def key(item: UserDTO):
        item = UserDTO.model_validate(item)
        return item.created_at

    sorted_items = items.copy()
    sorted_items.sort(key=key, reverse=True)
    index = 0
    while is_sorted and index < len(items):
        i = UserDTO.model_validate(items[index])
        j = UserDTO.model_validate(sorted_items[index])
        if i.id != j.id:
            is_sorted = False

        index = index + 1

    assert not is_sorted

    # check desc
    is_sorted = True
    order = "ASC"
    # assert order == "DESC"




# def test_get_user(client: TestClient, user_data: Dict) -> None:
#     _user_data = user_data.copy()
#     _user_data["email"] = "getthisuser@example.com"
#     response = client.post("/users", json=_user_data)
#     assert response.status_code == 200
#     body = response.json()
#     id = body.get("id")
#     response = client.get(
#         f"/users/{id}",
#         headers=mock_auth_header(client=client, user_data=_user_data),
#     )
#     assert response.status_code == 200
#     body = response.json()
#     assert body.get("id") == id
#     assert body.get("email") == "getthisuser@example.com"
#     assert body.get("created_at") and body.get("updated_at")
#
#
# def test_get_user_missing(client: TestClient, user_data: Dict) -> None:
#     _user_data = user_data.copy()
#     _user_data["email"] = "getmissing@example.com"
#     response = client.post("/users", json=_user_data)
#     assert response.status_code == 200
#     response = client.get(
#         f"/users/{uuid.uuid4()}",
#         headers=mock_auth_header(client=client, user_data=_user_data),
#     )
#     assert response.status_code == 400
#
#
# def test_list_users(client: TestClient, user_data: Dict) -> None:
#     _user_data = user_data.copy()
#     _user_data["email"] = "listusers@example.com"
#     response = client.post("/users", json=_user_data)
#     assert response.status_code == 200
#     response = client.get(
#         "/users",
#         headers=mock_auth_header(client=client, user_data=_user_data),
#     )
#     assert response.status_code == 200
#     body = response.json()
#     assert type(body) == list
#
#
# def test_update_user(client: TestClient, user_data: Dict) -> None:
#     _user_data = user_data.copy()
#     _user_data["email"] = "updateme@example.com"
#     response = client.post("/users", json=_user_data)
#     assert response.status_code == 200
#     assert response.json()["email"] == "updateme@example.com"
#     _update_body = user_data.copy()
#     _update_body["email"] = "newemail@example.com"
#     response = client.put(
#         "/users",
#         json=_update_body,
#         headers=mock_auth_header(client=client, user_data=_user_data),
#     )
#     assert response.status_code == 200
#     body = response.json()
#     assert body.get("id")
#     assert body.get("created_at") < body.get("updated_at")
#     assert body.get("email") == "newemail@example.com"
#
#
# def test_update_user_no_duplicate_emails(client: TestClient, user_data: Dict) -> None:
#     _user_data = user_data.copy()
#     _user_data["email"] = "canttouchthis@example.com"
#     response = client.post("/users", json=_user_data)
#     assert response.status_code == 200
#
#     _user_data = user_data.copy()
#     _user_data["email"] = "tryingtotouchthis@example.com"
#     response = client.post("/users", json=_user_data)
#     assert response.status_code == 200
#     assert response.json()["email"] == "tryingtotouchthis@example.com"
#
#     _update_body = user_data.copy()
#     _update_body["email"] = "canttouchthis@example.com"
#     response = client.put(
#         "/users",
#         json=_update_body,
#         headers=mock_auth_header(client=client, user_data=_user_data),
#     )
#     assert response.status_code == 422
#     assert response.json().get("detail") == "This email is taken. Try another."
#
#
# def test_delete_user(client: TestClient, user_data: Dict) -> None:
#     _user_data = user_data.copy()
#     _user_data["email"] = "deleteme@example.com"
#     response = client.post("/users", json=_user_data)
#     assert response.status_code == 200
#
#     response = client.delete(
#         "/users", headers=mock_auth_header(client=client, user_data=_user_data)
#     )
#     assert response.status_code == 200
#
#
# def test_bio_too_long(client: TestClient, user_data: Dict) -> None:
#     _user_data = user_data.copy()
#     _user_data["bio"] = "?" * 100 * 100
#     response = client.post("/users", json=_user_data)
#     assert response.status_code == 422
#     assert response.json().get("detail")[0].get("msg") == "Bio is too long."
#
#
# def test_bad_password(client: TestClient, user_data: Dict) -> None:
#     _user_data = user_data.copy()
#     _user_data["email"] = "badpass@example.com"
#     _user_data["password_hash"] = "short"
#     response = client.post("/users", json=_user_data)
#     assert response.status_code == 422
#     assert response.json().get("detail") == (
#         "Password must be 8 characters or more and have a mix of uppercase, "
#         "lowercase, numbers, and special characters."
#     )
