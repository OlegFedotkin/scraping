NAVIGATION_SELECTORS = {
    "parse_item": '//div[@class="vacancy-serp"]'
    '/div[contains(@data-qa, "vacancy-serp__vacancy")]'
    '//a[contains(@data-qa, "vacancy-title")]/@href',
    "parse": '//a[contains(@data-qa, "pager-next")]/@href',
    "parse_item_sj": '//div[contains(@class, "f-test-search-result-item")]//a[contains(@class, "f-test-link") and @target="_blank"]/@href',
    "parse_sj": '//a[contains(@class, "f-test-link-Dalshe")]/@href',
}

ITEM_SELECTORS = {
    "title": "//h1/text()",
    "salary": '//p[contains(@class,"vacancy-salary")]//text()',
}

ITEM_SELECTORS_SJ = {
    "title": "//h1/text()",
    "salary": '//div[contains(@class, "f-test-vacancy-base-info")]/*/following-sibling::*[1]/*/*/*/*/following-sibling::*[4]/*/*//text()',
}

# complex way
ITEM_ACTIONS = {
    "title": lambda response: response.xpath(ITEM_SELECTORS["title"]).get(),
    "salary": lambda response: response.xpath(ITEM_SELECTORS["salary"]).getall(),
}