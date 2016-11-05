# -*- coding: UTF-8 -*-

config = {
    'database': {
        'mongo': {
            'server': '185.99.214.188',
            'port': 28017
        }
    },
    'searchers': {
            'digikala': {
                'enabled': True,
                'class': 'DigikalaSearcher',
                'module': 'main.resources.searchers.digikala_searcher',
                'base_url': 'http://search.digikala.com/api/search',
                'phrases': ['ps4_games', 'camera_flash', 'mirrorless_camera', 'large_external_hdd'],
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
                    },
                    'large_external_hdd': {
                        'category': 'c68',
                        'type': '',
                        'attributes': ['A606V1074', 'A606V1075', 'A606V1518', 'A606V1519', 'A606V18497', 'A606V30937']
                    }
                }
            },
            'digikala_special_items': {
                'enabled': True,
                'class': 'DigikalaSpecialOfferSearch',
                'module': 'main.resources.searchers.digikala_special_offers',
                'base_url': 'http://search.digikala.com/api2/Data/Get?categoryId=0&ip=0',
            },
            'sheypoor': {
                'enabled': True,
                'class': 'SheypoorSearcher',
                'module': 'main.resources.searchers.sheypoor_searcher',
                'base_url': 'http://www.sheypoor.com/search',
                'phrases': ['fujifilm', 'fuji', 'fujinon', 'فوجی', 'فوجی فیلم', 'yongnuo']
            },
            'divar': {
                'enabled': True,
                'class': 'DivarSearcher',
                'module': 'main.resources.searchers.divar_searcher',
                'base_url': 'https://search.divar.ir/json/',
                'phrases': ['fujifilm', 'fuji', 'fujinon', 'فوجی', 'فوجی فیلم', 'yongnuo']
            },
            'afrang_timeline': {
                'enabled': True,
                'class': 'AfrangSecondHandTimelineSearcher',
                'module': 'main.resources.searchers.afrang_second_hand_timeline',
                'base_url': 'http://www.afrangdigital.com/Useds/-1',
                'phrases': ['fujifilm', 'fuji', 'fujinon', 'فوجی', 'فوجی فیلم', 'yongnuo']
            },
            'afrang': {
                'enabled': False,
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
