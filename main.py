# coding=utf-8
from __future__ import unicode_literals
from linkedin import Linkedin
import company
import time

if __name__ == '__main__':
    lnkdn = Linkedin(
        session_key='qa.andersen@gmail.com',
        session_password='qq111111',
    )

    search_query = 'vsearch/c?type=companies&orig=FCTD&rsid=2316940301413880758057' \
                   '&pageKey=member-home&search=Search&f_I=96&pt=companies&f_CCR=nl' \
                   '%3A0&openFacets=N,CCR,JO,I,CS&f_CS=D,E,F,G,C'

    lnkdn.set_search_query(search_query)
    lnkdn.navigate_search_page()

    entity_ids = lnkdn.get_entity_ids_from_current_page()
    companies = [company.get_company(e) for e in entity_ids]
    for c in companies:
        lnkdn.db.add_to_db(c)

    del entity_ids
    del companies

    while not '100' in lnkdn.get_current_page():

        time.sleep(15)
        lnkdn.navigate_next_page()
        time.sleep(15)

        entity_ids = lnkdn.get_entity_ids_from_current_page()
        companies = [company.get_company(e) for e in entity_ids]
        for c in companies:
            lnkdn.db.add_to_db(c)

        del entity_ids
        del companies

    print 'finished.'
