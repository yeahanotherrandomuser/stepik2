from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):
    def add_product_to_basket(self):
        self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BUTTON).click()

    def get_product_name(self):
        return self.get_element_text(*ProductPageLocators.PRODUCT_NAME)

    def get_product_price(self):
        return self.get_element_text(*ProductPageLocators.PRODUCT_PRICE)

    def should_be_basket_total_equal_to_price(self, expected_price):
        basket_total = self.get_element_text(*ProductPageLocators.BASKET_TOTAL_IN_MESSAGE)
        assert basket_total == expected_price, \
            f"Basket total '{basket_total}' differs from product price '{expected_price}'"

    def should_be_product_name_in_success_message(self, expected_name):
        name_in_message = self.get_element_text(*ProductPageLocators.PRODUCT_NAME_IN_MESSAGE)
        assert name_in_message == expected_name, \
            f"Name in message '{name_in_message}' differs from product name '{expected_name}'"

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Success message is presented, but should not be"

    def success_message_should_disappear(self):
        assert self.is_disappeared(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Success message did not disappear, but should have"
