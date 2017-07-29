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
                "base_url": "https://search.digikala.com/api/SearchApi",
                "phrases": ["sample_conf"],
                "phrase_details": {
                    "sample_conf": {
                        "urlCode": "url_code_from_digikala",
                        "brands": ["15", "10"],
                        "types": ["8", "12"],
                        "attributes": {
                            "4": ["1", "2"],
                            "6": ["2", "4"]
                        }
                    }
                }
            },
            "digikala_special_items": {
                "enabled": True,
                "class": "DigikalaSpecialOfferSearch",
                "module": "main.resources.searchers.digikala_special_offers",
                "base_url": "http://search.digikala.com/api2/Data/Get?categoryId=0&ip=0"
            },
            "sheypoor": {
                "enabled": True,
                "class": "SheypoorSearcher",
                "module": "main.resources.searchers.sheypoor_searcher",
                "base_url": "http://www.sheypoor.com/search",
                "phrases": ["fujifilm", "fuji", "fujinon", "فوجی", "فوجی فیلم", "yongnuo", "MJLQ2", "MJLT2"]
            },
            "divar": {
                "enabled": True,
                "class": "DivarSearcher",
                "module": "main.resources.searchers.divar_searcher",
                "base_url": "https://search.divar.ir/json/",
                "phrases": ["fujifilm", "fuji", "fujinon", "فوجی", "فوجی فیلم", "yongnuo", "MJLQ2", "MJLT2"]
            },
            "afrang_timeline": {
                "enabled": True,
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
