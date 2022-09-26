
def CalculateDistance(lat, lon, distance):
    query = f'''select id, first_name, last_name, address, lat, lon, (2 * 3.14157 * 6371 / 360.0)*sqrt((lat - {lat})*(lat - {lat}) + (lon - {lon})*(lon - {lon})) as distance from book_tbl
        where (2 * 3.14157 * 6371 / 360.0)*sqrt((lat - {lat})*(lat - {lat}) + (lon - {lon})*(lon - {lon})) < {distance}'''
    return query