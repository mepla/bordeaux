# -*- coding: UTF-8 -*-
import json
import logging

default_configs = {
    "database": {
        "mongo": {
            "server": "192.168.1.100",
            "port": 27017
        }
    },
    "searchers": {
            "digikala": {
                "enabled": True,
                "class": "DigikalaSearcher",
                "module": "main.resources.searchers.digikala_searcher",
                "base_url": "http://search.digikala.com/api/search",
                "phrases": ["mirrorless_camera", "camera_light", "4k_monitor", "gaming_mouse"],
                "phrase_details": {
                    "ps4_games": {
                        "category": "c5609",
                        "type": "4801"
                    },
                    "camera_light": {
                        "category": "c111",
                        "type": ""
                    },
                    "gopro_accessories": {
                        "category": "c1345",
                        "type": ""
                    },
                    "gopro": {
                        "category": "c49",
                        "type": "",
                        "brand": "76"
                    },
                    "camera_flash": {
                        "category": "c108",
                        "type": ""
                    },
                    "mirrorless_camera": {
                        "category": "c48",
                        "type": "8"
                    },
                    "large_external_hdd": {
                        "category": "c68",
                        "type": "242",
                        "attributes": [["A604V4378"], ["A606V1073"], ["A8670V7477"], ["A6516V4372"]]
                    },
                    "adsl-modem-5g": {
                        "category": "c5721",
                        "type": "",
                        "attributes": ["A18359V21726"]
                    },
                    "laptop_i7": {
                        "category": "c18",
                        "type": "",
                        "attributes": [["A303V432"], ["A308V32309", "A308V472", "A308V8560"]]
                    },
                    "mechanical_keyboard": {
                        "category": "c27",
                        "type": "5226"
                    },
                    "4k_monitor": {
                        "category": "c24",
                        "type": "",
                        "attributes": [["A23139V31332"]]
                    },
                    "gaming_mouse": {
                        "category": "c26",
                        "type": "6170"
                    }
                }
            },
            "digikala_special_items": {
                "enabled": False,
                "class": "DigikalaSpecialOfferSearch",
                "module": "main.resources.searchers.digikala_special_offers",
                "base_url": "http://search.digikala.com/api2/Data/Get?categoryId=0&ip=0",
            },
            "sheypoor": {
                "enabled": False,
                "class": "SheypoorSearcher",
                "module": "main.resources.searchers.sheypoor_searcher",
                "base_url": "http://www.sheypoor.com/search",
                "phrases": ["fujifilm", "fuji", "fujinon", "فوجی", "فوجی فیلم", "yongnuo", "MJLQ2", "MJLT2"]
            },
            "divar": {
                "enabled": False,
                "class": "DivarSearcher",
                "module": "main.resources.searchers.divar_searcher",
                "base_url": "https://search.divar.ir/json/",
                "phrases": ["fujifilm", "fuji", "fujinon", "فوجی", "فوجی فیلم", "yongnuo", "MJLQ2", "MJLT2"]
            },
            "afrang_timeline": {
                "enabled": False,
                "class": "AfrangSecondHandTimelineSearcher",
                "module": "main.resources.searchers.afrang_second_hand_timeline",
                "base_url": "http://www.afrangdigital.com/Useds/-1",
                "phrases": ["fujifilm", "fuji", "fujinon", "فوجی", "فوجی فیلم", "yongnuo"]
            },
            "afrang": {
                "enabled": False,
                "class": "AfrangSecondHandSearcher",
                "module": "main.resources.searchers.afrang_second_hand",
                "base_url": "http://www.afrangdigital.com/AjaxSearchUsed.aspx",
                "phrases": ["fujinon", "fujifilm", "xf 5", "xf 1", "xf 6", "xf 9"]
            }
    },
    "notifiers": {
        "email": {
            "from_address": "mepla.photography@gmail.com",
            "from_password": "XT2forthewin",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": "587",
            "to_address": "soheil.nasirian@gmail.com"
        }
    }
}

config_file_path = "/etc/bordeaux/bordeaux.conf"


def complete_config_file(default_config, config_file):
    for key, value in default_config.items():
        if key not in config_file:
            config_file[key] = value
        elif isinstance(value, dict):
            complete_config_file(value, config_file[key])
    return config_file


def load_config(path):
    try:
        configs_to_return = json.load(open(path))
        configs_to_return = complete_config_file(default_configs, configs_to_return)
    except IOError as exc:
        logging.warning("Config file does not exist at path: {} -> Default configs loaded.".format(path))
        configs_to_return = default_configs
    except Exception as exc:
        logging.critical("Config exists but could not be parsed: {}".format(exc))
        raise exc

    return configs_to_return

config = load_config(config_file_path)
