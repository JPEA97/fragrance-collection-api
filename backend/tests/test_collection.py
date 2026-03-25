def test_user_cannot_get_another_users_collection_item(
    client,
    auth_headers,
    seeded_catalog,
):
    headers_user_a = auth_headers(email="a@example.com", username="usera")
    headers_user_b = auth_headers(email="b@example.com", username="userb")

    create_response = client.post(
        "/collection/",
        json={
            "fragrance_id": seeded_catalog["fragrance"].id,
            "ownership_type": "full_bottle",
            "personal_rating": 8,
        },
        headers=headers_user_a,
    )

    assert create_response.status_code == 201
    item_id = create_response.json()["data"]["id"]

    get_response = client.get(
        f"/collection/{item_id}",
        headers=headers_user_b,
    )

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Collection item not found"


def test_user_cannot_patch_another_users_collection_item(
    client,
    auth_headers,
    seeded_catalog,
):
    headers_user_a = auth_headers(email="a@example.com", username="usera")
    headers_user_b = auth_headers(email="b@example.com", username="userb")

    create_response = client.post(
        "/collection/",
        json={
            "fragrance_id": seeded_catalog["fragrance"].id,
            "ownership_type": "full_bottle",
            "personal_rating": 8,
        },
        headers=headers_user_a,
    )

    assert create_response.status_code == 201
    item_id = create_response.json()["data"]["id"]

    patch_response = client.patch(
        f"/collection/{item_id}",
        json={"times_worn": 5},
        headers=headers_user_b,
    )

    assert patch_response.status_code == 404
    assert patch_response.json()["detail"] == "Collection item not found"


def test_user_cannot_delete_another_users_collection_item(
    client,
    auth_headers,
    seeded_catalog,
):
    headers_user_a = auth_headers(email="a@example.com", username="usera")
    headers_user_b = auth_headers(email="b@example.com", username="userb")

    create_response = client.post(
        "/collection/",
        json={
            "fragrance_id": seeded_catalog["fragrance"].id,
            "ownership_type": "full_bottle",
            "personal_rating": 8,
        },
        headers=headers_user_a,
    )

    assert create_response.status_code == 201
    item_id = create_response.json()["data"]["id"]

    delete_response = client.delete(
        f"/collection/{item_id}",
        headers=headers_user_b,
    )

    assert delete_response.status_code == 404
