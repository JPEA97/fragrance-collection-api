def test_list_fragrances_returns_catalog_items(client, db_session):
    from app.models.brand import Brand
    from app.models.fragrance import Fragrance

    brand = Brand(name="Chanel")
    db_session.add(brand)
    db_session.flush()

    fragrance = Fragrance(
        brand_id=brand.id,
        name="Bleu de Chanel",
        release_year=2010,
        gender_category="masculine",
        description="Versatile woody aromatic fragrance.",
    )
    db_session.add(fragrance)
    db_session.commit()

    response = client.get("/fragrances/")

    assert response.status_code == 200

    payload = response.json()
    assert "data" in payload
    assert "meta" in payload
    assert payload["meta"]["count"] == 1
    assert len(payload["data"]) == 1

    item = payload["data"][0]
    assert item["name"] == "Bleu de Chanel"
    assert item["brand"] == "Chanel"
    assert item["release_year"] == 2010
    assert item["gender_category"] == "masculine"


def test_list_fragrances_filters_by_brand(client, db_session):
    from app.models.brand import Brand
    from app.models.fragrance import Fragrance

    brand_1 = Brand(name="Chanel")
    brand_2 = Brand(name="Dior")
    db_session.add_all([brand_1, brand_2])
    db_session.flush()

    fragrance_1 = Fragrance(
        brand_id=brand_1.id,
        name="Bleu de Chanel",
        release_year=2010,
        gender_category="masculine",
        description="Test fragrance 1",
    )
    fragrance_2 = Fragrance(
        brand_id=brand_2.id,
        name="Dior Homme Intense",
        release_year=2011,
        gender_category="masculine",
        description="Test fragrance 2",
    )
    db_session.add_all([fragrance_1, fragrance_2])
    db_session.commit()

    response = client.get("/fragrances/?brand=Chanel")

    assert response.status_code == 200

    payload = response.json()
    assert payload["meta"]["count"] == 1
    assert len(payload["data"]) == 1
    assert payload["data"][0]["brand"] == "Chanel"
    assert payload["data"][0]["name"] == "Bleu de Chanel"


def test_list_fragrances_filters_by_search(client, db_session):
    from app.models.brand import Brand
    from app.models.fragrance import Fragrance

    brand = Brand(name="Chanel")
    db_session.add(brand)
    db_session.flush()

    fragrance_1 = Fragrance(
        brand_id=brand.id,
        name="Bleu de Chanel",
        release_year=2010,
        gender_category="masculine",
        description="Test fragrance 1",
    )
    fragrance_2 = Fragrance(
        brand_id=brand.id,
        name="Allure Homme Sport",
        release_year=2004,
        gender_category="masculine",
        description="Test fragrance 2",
    )
    db_session.add_all([fragrance_1, fragrance_2])
    db_session.commit()

    response = client.get("/fragrances/?search=bleu")

    assert response.status_code == 200

    payload = response.json()
    assert payload["meta"]["count"] == 1
    assert len(payload["data"]) == 1
    assert payload["data"][0]["name"] == "Bleu de Chanel"


def test_list_fragrances_search_is_accent_insensitive(client, db_session):
    from app.models.brand import Brand
    from app.models.fragrance import Fragrance

    brand = Brand(name="Lancôme")
    db_session.add(brand)
    db_session.flush()

    fragrance = Fragrance(
        brand_id=brand.id,
        name="Idôle",
        release_year=2019,
        gender_category="feminine",
        description="Accent-insensitive search test",
    )
    db_session.add(fragrance)
    db_session.commit()

    response = client.get("/fragrances/?brand=Lancome&search=Idole")

    assert response.status_code == 200

    payload = response.json()
    assert payload["meta"]["count"] == 1
    assert len(payload["data"]) == 1
    assert payload["data"][0]["brand"] == "Lancôme"
    assert payload["data"][0]["name"] == "Idôle"


def test_get_fragrance_detail_returns_item(client, db_session):
    from app.models.brand import Brand
    from app.models.fragrance import Fragrance

    brand = Brand(name="Prada")
    db_session.add(brand)
    db_session.flush()

    fragrance = Fragrance(
        brand_id=brand.id,
        name="L'Homme Prada",
        release_year=2016,
        gender_category="masculine",
        description="Polished iris-based fragrance.",
    )
    db_session.add(fragrance)
    db_session.commit()

    response = client.get(f"/fragrances/{fragrance.id}")

    assert response.status_code == 200

    payload = response.json()
    assert "data" in payload
    item = payload["data"]

    assert item["id"] == fragrance.id
    assert item["name"] == "L'Homme Prada"
    assert item["brand"] == "Prada"
    assert item["release_year"] == 2016
    assert item["gender_category"] == "masculine"
    assert item["description"] == "Polished iris-based fragrance."


def test_get_fragrance_detail_returns_404_for_missing_item(client):
    response = client.get("/fragrances/999999")

    assert response.status_code == 404
    assert response.json()["error"]["type"] == "http_error"
    assert response.json()["error"]["message"] == "Fragrance not found"
