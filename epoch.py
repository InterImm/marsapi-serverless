from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
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

        url = self.path
        parsed_url = urlparse(url)
        path = parsed_url.path
        epoch_time = path.split('/')[-1]
        epoch_time = int(float(epoch_time))

        mars_time = CoordinatedMarsTime.from_unix_time(epoch_time)
        mars_interimm_now = MartianTime()
        mars_interimm_now_hms = mars_interimm_now.interimm_clock(mars_time.msd)
        mars_interimm_now_cal = mars_interimm_now.interimm_calendar(mars_time.msd)

        dt_time = datetime.datetime.fromtimestamp(epoch_time).isoformat()

        res = {
            "earth_utc_time": dt_time,
            "mars_timezone": 0,
            "mars24": {
                'msd': mars_time.msd,
                'day': mars_time.days,
                'hour': mars_time.hours,
                'minute': mars_time.minutes,
                'second': mars_time.seconds,
                'millisecond': mars_time.milliseconds
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