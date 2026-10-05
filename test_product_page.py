import time

import pytest

from pages.basket_page import BasketPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

SITE = "http://selenium1py.pythonanywhere.com"
PRODUCT_LINK = f"{SITE}/catalogue/coders-at-work_207/"
PRODUCT_LINK_WITH_PROMO = f"{SITE}/catalogue/the-shellcoders-handbook_209/?promo=newYear"
PRODUCT_LINK_FOR_LOGIN_TESTS = f"{SITE}/en-gb/catalogue/the-city-and-the-stars_95/"
LOGIN_PAGE_LINK = f"{SITE}/en-gb/accounts/login/"
OFFER_LINK_TEMPLATE = f"{SITE}/catalogue/coders-at-work_207/?promo=offer{{}}"

# Promo number with the known site bug. Check it by running the parametrized test.
BUGGED_OFFER_NUMBER = 7
USER_PASSWORD = "Jh7#kd92Lq!x"


def build_offer_params():
    params = []
    for offer_number in range(10):
        marks = ()
        if offer_number == BUGGED_OFFER_NUMBER:
            marks = pytest.mark.xfail(reason="Known bug in the promo offer")
        params.append(pytest.param(OFFER_LINK_TEMPLATE.format(offer_number),
                                   marks=marks, id=f"offer{offer_number}"))
    return params


@pytest.mark.need_review
@pytest.mark.parametrize("link", build_offer_params())
def test_guest_can_add_product_to_basket(browser, link):
    page = ProductPage(browser, link)
    page.open()
    product_name = page.get_product_name()
    product_price = page.get_product_price()
    page.add_product_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_product_name_in_success_message(product_name)
    page.should_be_basket_total_equal_to_price(product_price)


def test_guest_should_see_login_link_on_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK_FOR_LOGIN_TESTS)
    page.open()
    page.should_be_login_link()


@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK_FOR_LOGIN_TESTS)
    page.open()
    page.go_to_login_page()
    login_page = LoginPage(browser, browser.current_url)
    login_page.should_be_login_page()


@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK_FOR_LOGIN_TESTS)
    page.open()
    page.go_to_basket_page()
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_not_be_items_in_basket()
    basket_page.should_be_empty_basket_message()


@pytest.mark.add_to_basket
class TestAddToBasketFromProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.link = PRODUCT_LINK

    @pytest.mark.xfail(reason="Success message appears right after adding the product")
    def test_guest_cant_see_success_message_after_adding_product_to_basket(self, browser):
        page = ProductPage(browser, self.link)
        page.open()
        page.add_product_to_basket()
        page.should_not_be_success_message()

    def test_guest_cant_see_success_message(self, browser):
        page = ProductPage(browser, self.link)
        page.open()
        page.should_not_be_success_message()

    @pytest.mark.xfail(reason="Success message does not disappear by itself")
    def test_message_disappeared_after_adding_product_to_basket(self, browser):
        page = ProductPage(browser, self.link)
        page.open()
        page.add_product_to_basket()
        page.success_message_should_disappear()


@pytest.mark.user_add_to_basket
class TestUserAddToBasketFromProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        login_page = LoginPage(browser, LOGIN_PAGE_LINK)
        login_page.open()
        email = str(time.time()) + "@fakemail.org"
        login_page.register_new_user(email, USER_PASSWORD)
        login_page.should_be_authorized_user()

    def test_user_cant_see_success_message(self, browser):
        page = ProductPage(browser, PRODUCT_LINK)
        page.open()
        page.should_not_be_success_message()

    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser):
        page = ProductPage(browser, PRODUCT_LINK_WITH_PROMO)
        page.open()
        product_name = page.get_product_name()
        product_price = page.get_product_price()
        page.add_product_to_basket()
        page.solve_quiz_and_get_code()
        page.should_be_product_name_in_success_message(product_name)
        page.should_be_basket_total_equal_to_price(product_price)
