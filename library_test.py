import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''


class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEqual(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # fourth unit test; prove that if we look for integers, we find four of them.
    def test_getdates(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

   # 5th unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_dates(self):
        self.assert_extract("no dates", library.dates_iso8601)

    # 6th unit test; prove that if we look for integers, we find four of them.
    def test_wordy_date(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')

    # 7
    def test_no_dates_for_fmt2(self):
        self.assert_extract("no dates", library.dates_fmt2)

    # 8
    def test_incorrect_format_for_fmt2(self):
        self.assert_extract("01/25/2017", library.dates_fmt2)

    # 9
    def test_DOW_included_for_fmt2(self):
        self.assert_extract('I was born on Mon, 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')

    # 10
    def test_isodates_with_time(self):
        self.assert_extract('I was born on 2015-07-25, 10:15AM', library.dates_iso8601, '2015-07-25')

    # 11
    def test_isodates_incorrect_format(self):
        self.assert_extract("01/25/2017", library.dates_iso8601)

    # 13
    def test_alice_needs_to_take_a_chill_pill(self):
        self.assert_extract("I couldn't work under such micromanaged environments :D", library.dates_iso8601)

    # 14
    def test_wordy_date_with_comma(self):
        self.assert_extract('I was born on 25 Jan, 2017.', library.dates_fmt2, '25 Jan, 2017')

    # 15
    def test_date_format_with_time(self):
        self.assert_extract("01/25/2017 10:18AM", library.dates_fmt2, "01/25/2017 10:18AM")

    # 16
    def test_date_format_with_24hr_time(self):
        self.assert_extract("01/25/2017 18:18", library.dates_fmt2, "01/25/2017 18:18")

    # 17
    def test_wordy_date_with_invalid_time(self):
        self.assert_extract("01/25/2017 99:78", library.dates_fmt2)

if __name__ == '__main__':
    unittest.main()
