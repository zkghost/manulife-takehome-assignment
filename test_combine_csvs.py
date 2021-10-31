import pytest

from combine_csvs import (
    get_csv_file_list,
    get_region_ips,
    parse_filename,
    write_output_csv, 
    OUTPUT_FILE
)

@pytest.mark.parametrize('test_input, expected',[
    # only keep csv files
    (['Asia Prod 1.csv', 'README.md', 'NA Prod.csv'], ['Asia Prod 1.csv', 'NA Prod.csv']),
    # dont keep output file
    (['EU Prod 2.csv', OUTPUT_FILE], ['EU Prod 2.csv'])
])
def test_get_csv_filelist( test_input, expected):
    actual = get_csv_file_list(test_input)
    print(f'test: {test_input}, expected: {expected}')
    assert actual == expected

@pytest.mark.parametrize('test_input, expected', [
    # ending and digit should be trimmed
    ('Asia Prod 1.csv', 'Asia Prod'),
    # same should apply for big numbers
    ('Asia Prod 9000000000000.csv', 'Asia Prod'),
    # ok if csv suffix not present to parse name
    ('Asia Prod 1', 'Asia Prod'), 
    # empty string should come back as is
    ('', ''),
    # if filename is just number, return empty str
    ('9', '')
])
def test_parse_filename(test_input, expected):
    actual = parse_filename(test_input)
    assert actual == expected
    
@pytest.mark.parametrize('test_input, expected', [
    # header row should get removed
    ([('Source IP,Count,Events per Second'),
      ('1.1.1.1', '1', '100'), 
      ('2.2.2.2', '1', '1000')], ['1.1.1.1', '2.2.2.2']),
])
def test_get_region_ips(test_input, expected):
    actual = get_region_ips(test_input)
    assert actual == expected
    