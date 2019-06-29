from http.server import BaseHTTPRequestHandler
import json
import debugserver
import datetime
from functions.mars import CoordinatedMarsTime
from functions.interimm import MartianTime

class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        mars_now = CoordinatedMarsTime.now()
        mars_interimm_now = MartianTime()
        mars_interimm_now_hms = mars_interimm_now.interimm_clock(mars_now.msd)
        mars_interimm_now_cal = mars_interimm_now.interimm_calendar(mars_now.msd)

        dt_now = datetime.datetime.utcnow().isoformat()

        res = {
            "earth_utc_time": dt_now,
            "mars_timezone": 0,
            "mars24": {
                'msd': mars_now.msd,
                'day': mars_now.days,
                'hour': mars_now.hours,
                'minute': mars_now.minutes,
                'second': mars_now.seconds,
                'millisecond': mars_now.milliseconds
            },
            "interimm": {
                "msd": mars_interimm_now_hms.get('msd'),
                "year": mars_interimm_now_cal.get('year'),
                "month": mars_interimm_now_cal.get('month'),
                "day": mars_interimm_now_cal.get('day'),
                "hour": mars_interimm_now_hms.get('hour'),
                "minute": mars_interimm_now_hms.get('minute'),
                "second": mars_interimm_now_hms.get('second')
            }
        }

        self.wfile.write(json.dumps(res).encode("utf-8"))

        return

if __name__ == '__main__':
    debugserver.serve(handler)