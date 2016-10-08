config = {
    'searchers': {
            'digikala': {
                'class': 'DigikalaSearcher',
                'module': 'main.resources.searchers.digikala_searcher',
                'base_url': 'http://search.digikala.com/api/search',
                'phrases': ['ps4_games']
            },
            'afrang': {
                'class': 'AfrangSecondHandSearcher',
                'module': 'main.resources.searchers.afrang_second_hand',
                'base_url': 'http://www.afrangdigital.com/AjaxSearchUsed.aspx',
                'phrases': ['fujinon', 'fujifilm', 'xf 5', 'xf 1', 'xf 6', 'xf 9']
            }
    },
    'notifiers': {
        'email': {
            'from_address': 'mepla.photography@gmail.com',
            'from_password': 'XT2forthewin',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': '587',
            'to_address': 'soheil.nasirian@gmail.com'
        }
    }
}
