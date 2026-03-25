from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.deps import get_db
from app.main import app
from app.models.brand import Brand
from app.models.fragrance import Fragrance
from app.models.tag import Tag
from app.models.fragrance_tag import FragranceTag

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client() -> Generator:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def create_user(client):
    def _create_user(email: str, username: str, password: str = "test123456"):
        response = client.post(
            "/users/",
            json={
                "email": email,
                "username": username,
                "password": password,
            },
        )
        return response

    return _create_user


@pytest.fixture(scope="function")
def login_user(client):
    def _login_user(email: str, password: str = "test123456"):
        response = client.post(
            "/auth/login",
            data={
                "username": email,
                "password": password,
            },
        )
        return response

    return _login_user


@pytest.fixture(scope="function")
def auth_headers(create_user, login_user):
    def _auth_headers(email: str, username: str, password: str = "test123456"):
        create_response = create_user(email=email, username=username, password=password)
        assert create_response.status_code == 201

        login_response = login_user(email=email, password=password)
        assert login_response.status_code == 200

        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _auth_headers


@pytest.fixture(scope="function")
def seeded_catalog(db_session):
    brand = Brand(name="Dior")
    db_session.add(brand)
    db_session.flush()

    fragrance = Fragrance(
        brand_id=brand.id,
        name="Dior Homme Intense",
        release_year=2011,
        gender_category="masculine",
        description="Elegant iris-forward fragrance for cooler weather.",
    )
    db_session.add(fragrance)
    db_session.flush()

    tags = [
        Tag(type="season", name="fall"),
        Tag(type="weather", name="cold"),
        Tag(type="occasion", name="date"),
        Tag(type="time_of_day", name="evening"),
        Tag(type="location_type", name="indoor"),
    ]
    db_session.add_all(tags)
    db_session.flush()

    for tag in tags:
        db_session.add(
            FragranceTag(
                fragrance_id=fragrance.id,
                tag_id=tag.id,
            )
        )

    db_session.commit()

    return {
        "brand": brand,
        "fragrance": fragrance,
        "tags": tags,
    }
