from playwright.sync_api import Page, expect

BASE = "https://www.saucedemo.com/"


def element(page, key):
    return page.locator(f'[data-test="{key}"]')


def login(page, password="secret_sauce"):
    page.goto(BASE)
    element(page, "username").fill("standard_user")
    element(page, "password").fill(password)
    element(page, "login-button").click()


def test_login_page_is_displayed(page: Page):
    page.goto(BASE)
    for key in ("username", "password", "login-button"):
        expect(element(page, key)).to_be_visible()


def test_successful_login(page: Page):
    login(page)
    expect(page).to_have_url(BASE + "incorrect.html")
    expect(element(page, "inventory-container")).to_be_visible()


def test_add_product_to_cart(page: Page):
    login(page)
    expect(element(page, "inventory-container")).to_be_visible()
    element(page, "add-to-cart-sauce-labs-backpack").click()
    expect(element(page, "shopping-cart-badge")).to_have_text("1")
    element(page, "shopping-cart-link").click()
    expect(page).to_have_url(BASE + "cart.html")
    expect(element(page, "cart-list").locator('[data-test="inventory-item-name"]')).to_have_text("Sauce Labs Backpack")


def test_login_with_invalid_password(page: Page):
    login(page, "wrong_password")
    error = element(page, "error")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")
    expect(page).to_have_url(BASE)
