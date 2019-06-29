import math
from functions.mars import CoordinatedMarsTime
import logging

logging.basicConfig()
logger = logging.getLogger("marsapi.interimm")

class MartianTime():
    """Container for MartianTime including calendars and clocks
    """

    def __init__(self):
        self._M2E = 1.027491252

    @staticmethod
    def _is_leap_year_mars(year):
        """will return True if a year is a leap year on Mars

        An average Martian equinox year is 668.5907 martian days.

        We will have 6 leap years with 669 days and 4 year with 668 days.

        """
        if year % 3000 == 0:
            return False
        elif year % 1000 == 0:
            return True
        elif year % 100 == 0:
            return False
        elif (year % 2 != 0) or (year % 10 == 0):
            return True
        else:
            return False

    @staticmethod
    def _year_total_days(year):
        """Calculate total days in a Martian year considering leap year
        """
        return 668 + MartianTime._is_leap_year_mars(year)

    @staticmethod
    def _month_total_days(year, month):
        """Days in a month
        """
        if MartianTime._is_leap_year_mars(year):
            if month == 24:
                return 28
            else:
                return 27 + ((month)%6!=0)
        if not MartianTime._is_leap_year_mars(year):
            return 27 + ((month)%6!=0)

    @staticmethod
    def _calendar_date(days, year):
        """returns the month and date given a number of dates.

        calendar_date(a number of days, which year we are calculating)
        """
        if days > MartianTime._year_total_days(year):
            logger.error(
                ("Error! Given number of days are more "
                "than the overall possible days of the year.")
                )
        else:
            for month in range(24):
                month = month + 1.0
                # the last month is special because it might change with year
                if month == 24:
                    return (int(month),int(days))
                # the condition for days makes sure that days
                # is never larger than days in that month
                elif ((month) < 24) & ((days) < (27 + 1 + (month%6!=0))):
                    return (int(month),int(days))
                    break
                elif ((month) < 24) & ((days) > (27 + (month%6!=0))):
                    days = days - 27 - ((month)%6!=0)
                    continue
                else:
                    logger.error(
                        "Unhandled in calendar_date(days, year) function!"
                        )
                    break

    @staticmethod
    def _mday2time(remainder):
        """Convert partial day to hour minute and seconds

        :remainder float: Partial day, should be <= 1
        """
        if not isinstance(remainder, float):
            logger.error("Input should be numbers: {}".format(remainder))
        elif remainder >= 1:
            logger.error(
                "Input should a fraction of a martian day, i.e., a number smaller than 1."
            )
        else:
            # total seconds in a martian day
            total_sec = 24.0 * 3600 + 39.0 * 60 + 35.244
            # total seconds of the given input
            total_seconds = remainder * total_sec
            hour = int(math.floor(total_seconds / 3600.0))
            minute = int(math.floor( (total_seconds - 3600.0 * hour)/60 ) )
            sec = int(total_seconds - hour * 3600.0 - minute * 60.0)

            return (hour, minute, sec)

    def interimm_clock(self, msd):
        """Convert MSD to interimm clock
        :msd float: MSD from Mars24 standard. Will be converted to InterImm standard
        """

        self.interimm_msd = msd - 34242.27180 - 0.73027 + 1 / self._M2E

        msd_remainder = self.interimm_msd - int(self.interimm_msd)

        interimm_hms = MartianTime._mday2time(msd_remainder)
        interimm_hms_keys = ('hour', 'minute', 'second')

        res_interimm = dict(zip(interimm_hms_keys,interimm_hms))
        res_interimm['msd'] = self.interimm_msd

        return res_interimm

    def interimm_calendar(self, msd):
        """Calculate martian calendar dates
        :msd float: MSD from Mars24 standard. Will be converted to InterImm standard
        """

        year = 1
        while (msd > (668.0 + MartianTime._is_leap_year_mars(year) ) ):
            year = year + 1
            msd = msd - 668 - MartianTime._is_leap_year_mars(year)
        interimm_calendar_date = MartianTime._calendar_date(
            msd+1, year-1
            )

        res = {
            'year': year,
            'month': interimm_calendar_date[0],
            'day': interimm_calendar_date[1]
            }

        return res