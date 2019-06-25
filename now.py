from http.server import BaseHTTPRequestHandler
import json
import debugserver
import datetime
from functions.mars import CoordinatedMarsTime

class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        mars_now = CoordinatedMarsTime.now()

        dt_now = datetime.datetime.utcnow().isoformat()

        res = {
            "earth_utc_time": dt_now,
            "mars_timezone": 0,
            "martian_standard": {
                'day': mars_now.days,
                'hour': mars_now.hours,
                'minute': mars_now.minutes,
                'second': mars_now.seconds,
                'millisecond': mars_now.milliseconds
            }
        }

        self.wfile.write(json.dumps(res).encode("utf-8"))

        return

if __name__ == '__main__':
    debugserver.serve(handler)