from app.api.common.schemas.navigation_links import NavigationLinks

def test_navigation_links_build_basic():
    links = NavigationLinks.build(
        request_path="/items",
        offset=10,
        limit=10,
        has_next=True,
        filters=None,
        sorting=None,
    )
    assert links.previous == "/items?_offset=0&_limit=10"
    assert links.current == "/items?_offset=10&_limit=10"
    assert links.next == "/items?_offset=20&_limit=10"

def test_navigation_links_build_with_filters_and_sorting():
    links = NavigationLinks.build(
        request_path="/produtos",
        offset=20,
        limit=10,
        has_next=True,
        filters="category=tv",
        sorting="name"
    )
    assert links.previous == "/produtos?_offset=10&_limit=10&category=tv&_sort=name"
    assert links.current == "/produtos?_offset=20&_limit=10&category=tv&_sort=name"
    assert links.next == "/produtos?_offset=30&_limit=10&category=tv&_sort=name"

def test_navigation_links_build_no_next():
    links = NavigationLinks.build(
        request_path="/produtos",
        offset=0,
        limit=10,
        has_next=False,
        filters=None,
        sorting=None
    )
    assert links.previous == "/produtos?_offset=0&_limit=10"
    assert links.current == "/produtos?_offset=0&_limit=10"
    assert links.next is None

def test_navigation_links_build_offset_less_than_zero():
    links = NavigationLinks.build(
        request_path="/produtos",
        offset=5,
        limit=10,
        has_next=True,
        filters=None,
        sorting=None
    )
    # prev_offset deve ser 0, nunca negativo
    assert links.previous == "/produtos?_offset=0&_limit=10"
    assert links.current == "/produtos?_offset=5&_limit=10"
    assert links.next == "/produtos?_offset=15&_limit=10"