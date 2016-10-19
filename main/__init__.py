# -*- coding: UTF-8 -*-

config = {
    'database': {
        'mongo': {
            'server': '192.168.1.100',
            'port': 27017
        }
    },
    'searchers': {
            'digikala': {
                'enabled': True,
                'class': 'DigikalaSearcher',
                'module': 'main.resources.searchers.digikala_searcher',
                'base_url': 'http://search.digikala.com/api/search',
                'phrases': ['ps4_games', 'camera_flash', 'mirrorless_camera'],
                'phrase_details': {
                    'ps4_games': {
                        'category': 'c5609',
                        'type': '4801'
                    },
                    'camera_flash': {
                        'category': 'c108',
                        'type': ''
                    },
                    'mirrorless_camera': {
                        'category': 'c48',
                        'type': '8'
                    }
                }
            },
            'afrang': {
                'enabled': False,
                'class': 'AfrangSecondHandSearcher',
                'module': 'main.resources.searchers.afrang_second_hand',
                'base_url': 'http://www.afrangdigital.com/AjaxSearchUsed.aspx',
                'phrases': ['fujinon', 'fujifilm', 'xf 5', 'xf 1', 'xf 6', 'xf 9']
            },
            'divar': {
                'enabled': True,
                'class': 'DivarSearcher',
                'module': 'main.resources.searchers.divar_searcher',
                'base_url': 'https://search.divar.ir/json/',
                'phrases': ['fujifilm', 'fuji', 'fujinon', 'فوجی', 'فوجی فیلم', 'yongnuo']
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
