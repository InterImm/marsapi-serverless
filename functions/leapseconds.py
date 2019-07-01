import json
import os

__cwd__ = os.getcwd()
__location__ = os.path.realpath(
    os.path.join(__cwd__, os.path.dirname(__file__))
    )

_LEAPSECONDS_JSON_PATH = os.path.join(
    __location__, 'leapseconds.json'
    )

def get_leapseconds():
    """Load leapseconds from json file
    """

    with open(_LEAPSECONDS_JSON_PATH, 'r') as fp:
        leapseconds_list = json.load(fp).get('data')

    leapseconds = []
    for i in leapseconds_list:
        leapseconds.append(
            (
                int(float(
                    i.get('epoch')
                    )),
                    int(
                        float(
                            i.get('seconds')
                        )
                        )
                )
            )

    return tuple(leapseconds)