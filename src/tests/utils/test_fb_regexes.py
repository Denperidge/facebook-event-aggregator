from src.facebook_event_aggregator.utils.fb_regexes import re_guests, re_line_with_characters, re_utc_and_more, re_three_letter_two_digit_date, re_utc_time, find_and_remove, regex_in

class TestFacebookRegexes():
    basic_string = "this is a string"
    complex_string = "Test! Meow!\nNOV\n11\nMore test!\nFri 19:00 UTC+01 AND 1 MORE\nName - 32 guests"
    
    def test_regex_in(self):
        assert regex_in(self.basic_string, r"[a-z]") == True
        assert regex_in(self.basic_string, r"[0-9]") == False
    

    def test_find_and_remove(self):
        remains, result = find_and_remove(self.basic_string, r"str.*ng")

        assert remains == "this is a "
        assert result == "string"

        remains, result = find_and_remove(self.basic_string, r"0.*9")

        assert remains == "this is a string"
        assert result == ""
    

    def test_re_line_with_characters(self):
        assert regex_in("Test", re_line_with_characters) == True
        assert regex_in("", re_line_with_characters) == False


    def test_re_utc_time(self):
        remains, result = find_and_remove(self.complex_string, re_utc_time)
        assert result == "Fri 19:00 UTC+01"


    def test_re_three_letter_two_digit_date(self):
        remains, result = find_and_remove(self.complex_string, re_three_letter_two_digit_date)
        assert result == "NOV\n11" 
        

    
    def test_re_guests(self):
        remains, result = find_and_remove(self.complex_string, re_guests)
        assert result == "Name - 32 guests"


    def test_re_utc_and_more(self):
        remains, result = find_and_remove(self.complex_string, re_utc_and_more)
        assert result == "UTC+01 AND 1 MORE"