blacklist = ["linkedin.com", "facebook.com", "pinterest.com", "angi.com", "yelp.com", "nextdoor.com", "glassdoor.com", "tripadvisor.com", "wikipedia.com", "youtube.com", "books.google.com", "clutch.co",
             "buildzoom.com", "homeadvisor.com", "thebluebook.com", "indeed.com", "chegg.com", "dnb.com", "groupon.com", "trip.com", "mapquest.com", "yellowpages.com", "hotels.com", "waze.com", "manta.com",
             "hobbylobby.com","t-mobile.com","shopsettings.com","myshopify.com","publix.com","kroger.com","menards.com","pinterest.com","cvs.com","homedepot.com","walmart.com","dollartree.com","lowes.com",
             "ebay.com","target.com","etsy.com","in-n-out.com","tiffany.com","familydollar.com","acehardware.com","yelp.com","coca-cola.com","instagram.com","twitter.com",'amazon.com','nordstrom.com',
             "apple.com","costco.com","macys.com","khols.com","ikea.com","sears.com","buzzfeed.com","today.com"]

def validate(url):
    split_url = url.split("/")
    host = split_url[2]

    slug = split_url[3:]
    if '' in slug:
        slug.remove('')

        # blacklist
    for site in blacklist:
        if site.lower() in host.lower():
            return False

    # gov/edu
    if '.gov' in host.lower() or '.edu' in host.lower():
        return False

    forbidden = ['news','blog', 'stories']

    for forbid in forbidden:
        if forbid.lower() in url:
            return False

    # # city/state in slug
    # for bit in slug:
    #     if len(bit) > 35:
    #         return False
    #     bit_mod = bit.lower().replace('-','').replace('_','').replace("'",'')
    #     for forbid in forbidden:
    #         forbid_mod = forbid.lower().replace('-','').replace('_','').replace("'",'')
    #         if forbid_mod in bit_mod:
    #             return False

    return True
