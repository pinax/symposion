from fixture_generator import fixture_generator

from symposion.sponsors_pro.models import SponsorLevel, Sponsor


SPONSORSHIP_LEVELS = [
    ("Diamond", 10000),
    ("Platinum", 5000),
    ("Gold", 2000),
    ("Silver", 1000),
    ("Patron", 500),
    ("Vendor I", 100),
    ("Media", 0),
]

SPONSORS = {
    "Diamond": [
        ("Google", "http://code.google.com/opensource/"),
    ],
    "Platinum": [
        ("CCP Games", "http://www.ccpgames.com/"),
    ],
    "Gold": [
        ("Walt Disney Animation Studios", "http://www.disneyanimation.com/"),
        ("neg-ng", "http://www.net-ng.com/"),
        ("socialserve.com", "http://www.socialserve.com/"),
        ("ActiveState", "http://www.activestate.com/"),
        ("White Oak", "http://www.woti.jobs/"),
        ("Canonical", "http://www.canonical.com/"),
        ("Microsoft", "http://ironpython.net/"),
        ("Sauce Labs", "http://www.saucelabs.com/"),
        ("Rackspace Cloud", "http://www.rackspacecloud.com/"),
        ("ESRI", "http://www.esri.com/"),
        ("Oracle", "http://wiki.oracle.com/page/Python"),
    ],
    "Silver": [
        ("Enthought", "http://www.enthought.com/"),
        ("Wingware", "http://www.wingware.com/"),
        ("Imaginary Landscape", "http://www.chicagopython.com/"),
        ("Emma", "http://www.myemma.com/"),
        ("Visual Numerics", "http://www.vni.com/"),
        ("Hiidef", "http://hiidef.com/"),
        ("Breadpig", "http://www.breadpig.com/"),
        ("Accense Technology", "http://www.accense.com/"),
        ("Tummy", "http://www.tummy.com/"),
    ],
    "Patron": [
        ("ZeOmega", "http://www.zeomega.com/"),
    ],
    "Vendor I": [
        ("O'Reilly", "http://www.oreilly.com/"),
    ],
    "Media": [
        ("Linux Journal", "http://www.linuxjournal.com/"),
        ("Linux Pro Magazine", "http://www.linuxpromagazine.com/"),
        ("Ubuntu User", "http://ubuntu-user.com/"),
        ("Code Magazine", "http://www.code-magazine.com/"),
        ("Startup Riot", "http://startupriot.com/"),
        ("Bit", "http://thebitsource.com/"),
    ]
}


@fixture_generator(SponsorLevel, Sponsor)
def pycon_2010_sponsors():
    levels = {}
    for pos, (name, cost) in enumerate(SPONSORSHIP_LEVELS):
        levels[name] = SponsorLevel.objects.create(order=pos, name=name, cost=cost)
    
    for level, sponsors in SPONSORS.iteritems():
        for name, url in sponsors:
            Sponsor.objects.create(
                name=name,
                external_url=url,
                level=levels[level]
            )
