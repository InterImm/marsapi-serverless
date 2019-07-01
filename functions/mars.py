import time
import sys
from functions.leapseconds import get_leapseconds as _get_leapseconds

LEAP_SECONDS = _get_leapseconds()

def _get_tai_offset_since(unix_time, leap_seconds=None):
    if leap_seconds is False:
        return 0
    tai_offset = 9
    if leap_seconds is None:
        leap_seconds = LEAP_SECONDS
    for t, new_tai_offset in leap_seconds:
        if t - 2208988800 <= unix_time:
            tai_offset = new_tai_offset
        else:
            break
    return tai_offset


class CoordinatedMarsTime(object):
    __slots__ = (
        '_days', '_hours', '_minutes', '_seconds', '_milliseconds',
        '_msd', '_ut'
    )

    def __init__(self, days, hours, minutes=0, seconds=0, milliseconds=0.):
        self._days = days
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds
        self._milliseconds = milliseconds
        self._msd = (
            days + (hours / 24.) + (minutes / (24 * 60.)) +
            (seconds / (24 * 60 * 60.)) +
            (milliseconds / (24 * 60 * 60 * 1000.))
        )
        self._ut = None

    @classmethod
    def from_mars_sol_day(cls, msd):
        """
        """
        mtc = msd % 1
        self = cls.__new__(cls)
        self._msd = msd
        self._days = int(msd)
        self._hours = int(mtc * 24)
        self._minutes = int(mtc * (24 * 60)) % 60
        self._seconds = int(mtc * (24 * 60 * 60)) % 60
        self._milliseconds = int(mtc * (24 * 60 * 60 * 1000)) % 1000
        self._ut = None

    @classmethod
    def from_unix_time(cls, unix_time, leap_seconds=None, round_milliseconds=True):
        """
        Creates a MarsTime from a unix time, as seconds from the Unix Epoch.
        leap_seconds should be a sorted sequence of (t, new_tai_offset)
        tuples, where new_tai_offset is the new value of TAI - UTC in seconds and
        t is the number of seconds since 00:00 1 January 1900 GMT that the leap
        second occurred. Defaults to mars_time.LEAP_SECONDS if not given.
        Leap seconds are ignored if it is set to False.
        """
        tai_offset = _get_tai_offset_since(unix_time, leap_seconds)
        msd = (unix_time + tai_offset) / 88775.244147 + 34127.2954262
        mtc = (
            (unix_time + tai_offset + 3029658983.5377016) % 88775.244147
        ) / 3698.968506125
        self = cls.__new__(cls)
        self._ut = unix_time
        self._msd = msd
        self._days = int(msd)
        self._hours = int(mtc)
        self._minutes = int(mtc * 60) % 60
        self._seconds = int(mtc * (60 * 60)) % 60
        milli = mtc * (60 * 60 * 1000) % 1000
        if round_milliseconds:
            milli = int(milli)
        self._milliseconds = milli
        return self

    @classmethod
    def now(cls, leap_seconds=None, round_milliseconds=True):
        return cls.from_unix_time(time.time(), leap_seconds, round_milliseconds)

    @property
    def msd(self):
        return self._msd

    @msd.setter
    def msd(self, value):
        mtc = value % 1
        self._days = int(value)
        self._hours = int(mtc * 24)
        self._minutes = int(mtc * (24 * 60)) % 60
        self._seconds = int(mtc * (24 * 60 * 60)) % 60
        self._milliseconds = int(mtc * (24 * 60 * 60 * 1000)) % 1000

        self._msd = value
        self._ut = None

    @property
    def days(self):
        return self._days

    @days.setter
    def days(self, value):
        days = int(value)
        if value != days:
            raise TypeError('days should be an integer')
        if days == self._days:
            return
        diff = days - self._days
        self._days = days
        self._msd += diff
        self._ut = None

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value):
        hours = int(value)
        if value != hours:
            raise TypeError('hours should be an integer')
        if hours == self._hours:
            return
        self._hours = hours
        self._msd = (
            self._days + (hours / 24.) + (self._minutes / (24 * 60.)) +
            (self._seconds / (24 * 60 * 60.)) +
            (self._milliseconds / (24 * 60 * 60 * 1000.))
        )
        self._ut = None

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        minutes = int(value)
        if value != minutes:
            raise TypeError('minutes should be an integer')
        if minutes == self.minutes:
            return
        self._minutes = minutes
        self._msd = (
            self._days + (self._hours / 24.) + (minutes / (24 * 60.)) +
            (self._seconds / (24 * 60 * 60.)) +
            (self._milliseconds / (24 * 60 * 60 * 1000.))
        )
        self._ut = None

    @property
    def seconds(self):
        return self._seconds

    @seconds.setter
    def seconds(self, value):
        seconds = int(value)
        if value != seconds:
            raise TypeError('seconds should be an integer')
        if seconds == self.seconds:
            return
        self._seconds = seconds
        self._msd = (
            self._days + (self._hours / 24.) + (self._minutes / (24 * 60.)) +
            (seconds / (24 * 60 * 60.)) +
            (self._milliseconds / (24 * 60 * 60 * 1000.))
        )
        self._ut = None

    @property
    def milliseconds(self):
        return self._milliseconds

    @milliseconds.setter
    def milliseconds(self, value):
        milliseconds = float(value)
        if value != milliseconds:
            raise TypeError('milliseconds should be a float')
        if milliseconds == self._milliseconds:
            return
        self._milliseconds = milliseconds
        self._msd = (
            self._days + (self._hours / 24.) + (self._minutes / (24 * 60.)) +
            (self._seconds / (24 * 60 * 60.)) +
            (milliseconds / (24 * 60 * 60 * 1000.))
        )
        self._ut = None

    @property
    def ut(self):
        if self._ut is not None:
            return self._ut
        tai = (self._msd - 34127.2954262) * 88775.244147

        # Can be up to 1 second off, rarely, but this is more
        # than the floating point error.
        ut = self._ut = tai - _get_tai_offset_since(tai)
        return ut

    @ut.setter
    def ut(self, value):
        new_self = CoordinatedMarsTime.from_unix_time(value)
        self._days = new_self._days
        self._hours = new_self._hours
        self._minutes = new_self._minutes
        self._seconds = new_self._seconds
        self._milliseconds = new_self._milliseconds
        self._msd = new_self._msd
        self._ut = new_self._ut

    def __repr__(self):
        return (
            '{type}(days={self.days}, hours={self.hours}, '
            'minutes={self.minutes}, seconds={self.seconds}, '
            'milliseconds={self.milliseconds})'
        ).format(type=type(self).__name__, self=self)


_FORMAT = (
    'Mars Sol Date: {0.days}; '
    'Coordinated Mars Time: {0.hours:02}:{0.minutes:02}:'
    '{0.seconds:02}.{0.milliseconds:03.0f}'
)

_MAIN_FORMAT = ('\r' + _FORMAT).format
_FORMAT = _FORMAT.format


def terminal_clock(file=sys.stdout, interval=0.01):
    # Lookup optimisations
    now = CoordinatedMarsTime.now
    fmt = _MAIN_FORMAT
    time_sleep = time.sleep
    file_write = file.write
    file_flush = file.flush
    try:
        file_write(_FORMAT(now()))
        file_flush()

        while True:
            time_sleep(interval)
            file_write(fmt(now(None, True)))
            file_flush()
    except KeyboardInterrupt:
        pass
        # Clean exit
    finally:
        file_write('\n')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            sys.exit(
                '0 or 1 arguments should be passed in the command line. '
                'See --help.'
            )
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print(
                'Continuously prints the time in Coordinated Mars Time (MTC). '
                'Pass "-x" to only print once, otherwise pass an interval '
                'to print the time in.'
            )
        elif sys.argv[1] == '-x':
            print(_FORMAT(CoordinatedMarsTime.now()))
        else:
            try:
                interval = float(sys.argv[1])
                if interval < 0:
                    raise ValueError
            except ValueError:
                sys.exit('"{}" could not be interpreted as a positive number'.format(sys.argv[1]))
            else:
                terminal_clock(interval=interval)
    else:
        terminal_clock(interval=0.01)