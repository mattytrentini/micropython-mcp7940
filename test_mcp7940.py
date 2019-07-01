import unittest
import mcp7940


class I2CTester:
    def __init__(self):
        self.register_data = {}

    def readfrom_mem(self, address, start, length):
        print("Read: {}: start at {}, length {}".format(address, start, length))
        if not set(list(range(start, length))).issubset(self.register_data.keys()):
            raise IndexError
        return bytes([self.register_data[start + i] for i in range(length)])

    def writeto_mem(self, address, start, bytes_to_write):
        print(
            "Write: {}: start at {}, bytes: {} ({})".format(
                address, start, bytes_to_write.hex(), len(bytes_to_write)
            )
        )
        for i, b in enumerate(bytes_to_write):
            self.register_data[start + i] = b


class TestMcp(unittest.TestCase):
    def test_i2c_tester(self):
        i2c_tester = I2CTester()

        data = bytes([1, 2, 3, 4])

        # Ensure data written can be written and read back
        i2c_tester.writeto_mem(0, 0, data)
        self.assertEqual(data, i2c_tester.readfrom_mem(0, 0, 4))

        # Ensure an exception is raised if reading a register that's not been written to
        with self.assertRaises(IndexError):
            i2c_tester.readfrom_mem(0, 0, 5)

    def test_bcd_conversions(self):
        bcd_int = (
            (0x00, 0),
            (0x02, 2),
            (0x09, 9),
            (0x10, 10),
            (0x11, 11),
            (0x44, 44),
            (0x99, 99),
        )
        for b, i in bcd_int:
            print(hex(b), i)
            self.assertEqual(mcp7940.MCP7940.bcd_to_int(b), i)
            self.assertEqual(mcp7940.MCP7940.int_to_bcd(i), b)

    def test_leap_years(self):
        """https://kalender-365.de/leap-years.php"""
        known_leap_years = [
            1804,
            1808,
            1812,
            1816,
            1820,
            1824,
            1828,
            1832,
            1836,
            1840,
            1844,
            1848,
            1852,
            1856,
            1860,
            1864,
            1868,
            1872,
            1876,
            1880,
            1884,
            1888,
            1892,
            1896,
            1904,
            1908,
            1912,
            1916,
            1920,
            1924,
            1928,
            1932,
            1936,
            1940,
            1944,
            1948,
            1952,
            1956,
            1960,
            1964,
            1968,
            1972,
            1976,
            1980,
            1984,
            1988,
            1992,
            1996,
            2000,
            2004,
            2008,
            2012,
            2016,
            2020,
            2024,
            2028,
            2032,
            2036,
            2040,
            2044,
            2048,
            2052,
            2056,
            2060,
            2064,
            2068,
            2072,
            2076,
            2080,
            2084,
            2088,
            2092,
            2096,
            2104,
            2108,
            2112,
            2116,
            2120,
            2124,
            2128,
            2132,
            2136,
            2140,
            2144,
            2148,
            2152,
            2156,
            2160,
            2164,
            2168,
            2172,
            2176,
            2180,
            2184,
            2188,
            2192,
            2196,
            2204,
            2208,
            2212,
            2216,
            2220,
            2224,
            2228,
            2232,
            2236,
            2240,
            2244,
            2248,
            2252,
            2256,
            2260,
            2264,
            2268,
            2272,
            2276,
            2280,
            2284,
            2288,
            2292,
            2296,
            2304,
            2308,
            2312,
            2316,
            2320,
            2324,
            2328,
            2332,
            2336,
            2340,
            2344,
            2348,
            2352,
            2356,
            2360,
            2364,
            2368,
            2372,
            2376,
            2380,
            2384,
            2388,
            2392,
            2396,
            2400,
        ]
        leap_years = [y for y in range(1800, 2401) if mcp9740.MCP7940.is_leap_year(y)]
        self.assertEqual(known_leap_years, leap_years)
        print(len(known_leap_years), len(leap_years))

    def test_set_time(self):
        i2c_tester = I2CTester()
        mcp = mcp7940.MCP7940(i2c_tester)

        now = (
            2019,
            7,
            16,
            15,
            29,
            14,
            6,
            167,
        )  # Sunday 2019/7/16 3:29:14pm (yearday=167)

        mcp.time = now
        self.assertEqual(mcp.time, now[:-1] + (0,))  # Return 0 for day of year

    def test_alarms(self):
        i2c_tester = I2CTester()
        mcp = mcp7940.MCP7940(i2c_tester)

        now = (
            2019,
            7,
            16,
            15,
            29,
            14,
            6,
            167,
        )  # Sunday 2019/7/16 3:29:14pm (yearday=167)

        mcp.alarm1 = now
        self.assertEqual(mcp.alarm1, now[1:-1])  # Drop year and yearday

        mcp.alarm2 = now
        self.assertEqual(mcp.alarm2, now[1:-1])  # Drop year and yearday
